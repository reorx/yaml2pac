#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import sys
import yaml
import json
import pkgutil
import logging
import argparse

from yaml2pac.core import convert_to_pac_args, print_stderr
from yaml2pac.testing import start_testing


def generate_pac(pac_args):
    pac_text = pkgutil.get_data('yaml2pac', 'data/template.pac')
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
    parser.add_argument(
            '-t', '--test', type=str, metavar='PAC',
            help=("Set system proxy using the PAC file then test its usability, "
                  "after this process the system proxy will be restored"))
    parser.add_argument(
            '--requester', type=str,
            help=("Executable to send HTTP request when doing PAC test,"
                  "this argument is required when `-t` is used."))

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Get yaml content
    try:
        with open(args.yaml, 'r') as f:
            text = f.read()
    except IOError as e:
        print_stderr('Could not read file {}: {}'.format(args.yaml, e))
        sys.exit()

    d = yaml.load(text)

    pac_args = convert_to_pac_args(d, ignore_warning=args.ignore)

    if args.test:
        if not args.requester:
            raise ValueError('`--requester` must be specified when `-t` is used.')
        start_testing(pac_args, args.test, args.requester)
    else:
        print(generate_pac(pac_args))


if __name__ == '__main__':
    main()
