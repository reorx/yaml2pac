#!/usr/bin/env python
# coding: utf-8

import sys
import yaml
import json


def _to_object(l, v):
    # although `direct:` rule set don't use `- <match>:proxy_name` directive,
    # use the same function to multiplex the code
    o = {}
    for i in l:
        if isinstance(i, basestring):
            o[i] = v
        elif isinstance(i, dict):
            _k, _v = i.items()[0]
            o[_k] = _v
    return o


def parse_default(default):
    if default == 'direct':
        return 'direct'
    elif default == 'proxy':
        return 'proxies["default"]'
    else:
        return 'proxies["%s"]' % default


def generate_pac(d):
    """
    Variables to replace:
        __PROXIES__
        __DEFAULT__
        __IP__
        __KEYWORD__
        __DOMAIN__
    """

    with open('template.pac', 'r') as f:
        template = f.read()

    rule_types = ['ip', 'keyword', 'domain']
    rule_values = {
        'direct': 0,
        'proxy': 1,
    }

    pac_args = {
        'proxies': d['meta']['proxies'],
        'default': parse_default(d['meta']['default']),
    }
    [pac_args.setdefault(i, {}) for i in rule_types]

    # handle rules
    for i, rule_value in rule_values.iteritems():
        ruleset = d.get(i)
        if not ruleset:
            continue
        for rule_type in rule_types:
            rules = ruleset.get(rule_type)
            if not rules:
                continue
            pac_args[rule_type].update(
                _to_object(rules, rule_value)
            )

    #print pac_args
    pac_text = template
    for i, j in pac_args.iteritems():
        key = '__' + i.upper() + '__'
        if i == 'default':
            value = j
        else:
            value = json.dumps(j, indent=4)
        pac_text = pac_text.replace(key, value)
    return pac_text


def write_pac(text, filename):
    with open(filename, 'w') as f:
        f.write(text)


if __name__ == '__main__':

    filename = sys.argv[1]

    with open(filename, 'r') as f:
        text = f.read()

    d = yaml.load(text)

    write_pac(generate_pac(d), sys.argv[2])
