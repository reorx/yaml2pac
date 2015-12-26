#!/usr/bin/env python
# coding: utf-8

import sys
import yaml
import json
import pkgutil
import argparse


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


def _parse_default(default):
    if default == 'direct':
        return 'direct'
    elif default == 'proxy':
        return 'proxy["default"]'
    else:
        return 'proxy["%s"]' % default


def generate_pac(d):
    """
    Variables to replace:
        __PROXIES__
        __DEFAULT__
        __IP__
        __KEYWORD__
        __DOMAIN__
    """
    template = pkgutil.get_data('yaml2pac', 'template.pac')

    rule_types = ['ip', 'keyword', 'domain']
    rule_values = {
        'direct': 0,
        'proxy': 1,
    }

    pac_args = {
        'proxy': d['meta']['proxy'],
        'default': _parse_default(d['meta']['default']),
    }
    [pac_args.setdefault(i, {}) for i in rule_types]

    # handle rules
    # for i, rule_value in rule_values.iteritems():
    for k, ruleset in d.iteritems():
        if k == 'meta':
            continue
        rule_value = rule_values.get(k, k)
        for rule_type in rule_types:
            rules = ruleset.get(rule_type)
            if not rules:
                continue
            pac_args[rule_type].update(
                _to_object(rules, rule_value)
            )

    # print pac_args
    pac_text = template
    for i, j in pac_args.iteritems():
        key = '__' + i.upper() + '__'
        if i == 'default':
            value = j
        else:
            value = json.dumps(j, indent=4)
        pac_text = pac_text.replace(key, value)
    return pac_text


def main():
    usage_example = """Example:
  yaml2pac myrules.yaml > ~/.ShadowsocksX/gfwlist.js"""

    parser = argparse.ArgumentParser(
        description="Generate pac content from yaml file",
        epilog=usage_example,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # arguments
    parser.add_argument('yaml', metavar="YAML", type=str, help="The input yaml file")

    args = parser.parse_args()

    try:
        with open(args.yaml, 'r') as f:
            text = f.read()
    except IOError as e:
        print 'Could not read file {}: {}'.format(args.yaml, e)
        sys.exit()

    d = yaml.load(text)

    print generate_pac(d)


if __name__ == '__main__':
    main()
