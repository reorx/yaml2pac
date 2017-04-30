#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import sys


RULE_TYPES = ['domain', 'keyword', 'ip']

RULE_VALUES = {
    'direct': 0,
    'proxy': 1,
}

SYSTEM_PROXY_HEADS = ['DIRECT', 'PROXY', 'SOCKS']


def convert_to_pac_args(d, rule_types=RULE_TYPES, rule_values=RULE_VALUES, ignore_warning=False):
    """
    Variables to replace:
        __PROXIES__
        __DEFAULT__
        __IP__
        __KEYWORD__
        __DOMAIN__

    Return `pac_args` like:
    {
        'default': 'direct',
        'proxies': {
            'default': 'SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080; DIRECT;',
            'https_1': 'HTTPS 1.your-proxy.io:443;'
        },
        'domain': {
            'a.com': 1,
            'c.come': 'https_1',
        },
        'keywords': {
            'b': 1,
            'd': 'https_1',
        },
        'ip': {
            '8.8.0.0/16': 1,
            '114.114.114.0/24': 'https_1'
        },
    }
    """

    proxies = d['meta']['proxy']

    # Check proxy compatibility
    for proxy in proxies.itervalues():
        is_compatible = check_proxy_compatibility(proxy)
        if not is_compatible and not ignore_warning:
            print_stderr('Proxy definition `{}` is not compatible with system PAC'.format(proxy))

    pac_args = {
        'proxies': proxies,
        'default': _get_default_js(d['meta']['default']),
    }
    [pac_args.setdefault(i, {}) for i in rule_types]

    # Naming convention:
    # In a typical yaml2pac yaml file:
    # ```
    # proxy:
    #   domain:
    #     - a.com
    #     - b.com
    #   keyword:
    #     - c
    # ```
    # The content of `proxy`, including both `domain` and `keyword`, is the `ruleset`;
    # Items of `domain` or `keyword` is the `rules`;
    for key, ruleset in d.iteritems():
        if key == 'meta':
            continue
        rule_value = rule_values.get(key, key)
        for rule_type in rule_types:
            rules = ruleset.get(rule_type)
            if not rules:
                continue
            pac_args[rule_type].update(
                rules_to_dict(rules, rule_value)
            )

    # print pac_args
    return pac_args


def rules_to_dict(l, v):
    """
    Convert rules like:
    - a.com
    - b.com: some_proxy
    to dict like:
    {
        'a.com': 1
        'b.com': 'some_proxy'
    }
    """
    o = {}
    for i in l:
        if isinstance(i, basestring):
            o[i] = v
        elif isinstance(i, dict):
            _k, _v = i.items()[0]
            o[_k] = _v
    return o


def _get_default_js(default):
    if default == 'direct':
        return 'direct'
    elif default == 'proxy':
        return 'proxy["default"]'
    else:
        return 'proxy["%s"]' % default


def _check_single_proxy_compatibility(proxy):
    for i in SYSTEM_PROXY_HEADS:
        if proxy.startswith(i):
            return True
    return False


def check_proxy_compatibility(proxy):
    is_compatible = False
    for i in proxy.split(';'):
        # As long as there's at least one compatible single proxy,
        # the whole proxy is compatible
        if _check_single_proxy_compatibility(i):
            is_compatible = True
    return is_compatible


def print_stderr(*args):
    print(*args, file=sys.stderr)
