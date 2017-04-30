#!/usr/bin/env python
# coding: utf-8

import yaml


text = """
a:
  a-b: xx
  c[d]: oo
e[f]:
  wtf
"""

print yaml.load(text)
