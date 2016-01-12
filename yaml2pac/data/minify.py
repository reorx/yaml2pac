#!/usr/bin/env python
# coding: utf-8

"""
This is a simple & incomplete implementation of javascript minify,
it requires the input javascript file to be strictly formatted,
like, `;` must be put every end of line, please don't use it outside of this project.
"""


def minify(fileobj):
    new_lines = []
    for line in fileobj.readlines():
        new_line = line.strip()
        if not new_line.startswith('//'):
            new_lines.append(new_line)
    return ''.join(new_lines)


if __name__ == '__main__':
    import sys

    input_file = sys.argv[1]
    with open(input_file, 'r') as f:
        print minify(f)
