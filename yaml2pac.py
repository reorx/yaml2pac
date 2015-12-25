#!/usr/bin/env python
# coding: utf-8

import yaml


with open('auto-ondemand.yaml', 'r') as f:
    text = f.read()

d = yaml.load(text)
print d
