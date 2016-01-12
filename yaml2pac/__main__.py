#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import sys
import yaml
import json
import pkgutil
import argparse


# TODO cidr matching https://github.com/skx/cidr_match.js


def print_stderr(*args):
    print(*args, file=sys.stderr)


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


def _parse_default(default):
    if default == 'direct':
        return 'direct'
    elif default == 'proxy':
        return 'proxy["default"]'
    else:
        return 'proxy["%s"]' % default



SYSTEM_PROXY_HEADS = ['DIRECT', 'PROXY', 'SOCKS']


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


RULE_TYPES = ['ip', 'keyword', 'domain']

RULE_VALUES = {
    'direct': 0,
    'proxy': 1,
}


def generate_pac(d, rule_types=RULE_TYPES, rule_values=RULE_VALUES, ignore_warning=False):
    """
    Variables to replace:
        __PROXIES__
        __DEFAULT__
        __IP__
        __KEYWORD__
        __DOMAIN__
    """
    template = pkgutil.get_data('yaml2pac', 'template.pac')

    proxies = d['meta']['proxy']

    # Check proxy compatibility
    for proxy in proxies.itervalues():
        is_compatible = check_proxy_compatibility(proxy)
        if not is_compatible and not ignore_warning:
            print_stderr('Proxy definition `{}` is not compatible with system PAC'.format(proxy))

    pac_args = {
        'proxies': proxies,
        'default': _parse_default(d['meta']['default']),
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
    pac_text = template
    for i, j in pac_args.iteritems():
        template_key = '__' + i.upper() + '__'
        if i == 'default':
            template_value = j
        else:
            template_value = json.dumps(j, indent=4)
        pac_text = pac_text.replace(template_key, template_value)
    return pac_text


def main():
    usage_example = """Example:
  yaml2pac myrules.yaml > ~/.ShadowsocksX/gfwlist.js"""

    parser = argparse.ArgumentParser(
        description="Generate pac file from yaml file",
        epilog=usage_example,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # arguments
    parser.add_argument('yaml', metavar="YAML", type=str, help="The input yaml file")

    # options
    parser.add_argument('-i', '--ignore', action='store_true',
                        help="Ignore warnings, no warnings will show up")

    args = parser.parse_args()

    try:
        with open(args.yaml, 'r') as f:
            text = f.read()
    except IOError as e:
        print_stderr('Could not read file {}: {}'.format(args.yaml, e))
        sys.exit()

    d = yaml.load(text)

    print(generate_pac(d, ignore_warning=args.ignore))


if __name__ == '__main__':
    main()
