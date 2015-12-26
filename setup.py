#!/usr/bin/env python
# coding=utf-8

from setuptools import setup


# Use semantic versioning: MAJOR.MINOR.PATCH
version = '0.1.0'


def get_requires():
    try:
        with open('requirements.txt', 'r') as f:
            requires = [i for i in map(lambda x: x.strip(), f.readlines()) if i]
        return requires
    except IOError:
        return []


def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except IOError:
        return ''


setup(
    # license='License :: OSI Approved :: MIT License',
    name='yaml2pac',
    version=version,
    author='reorx',
    author_email='novoreorx@gmail.com',
    description='Generate decent pac file from a set of yaml rules',
    url='https://github.com/reorx/yaml2pac',
    long_description=get_long_description(),
    packages=['yaml2pac'],
    # Or use (make sure find_packages is imported from setuptools):
    # packages=find_packages()
    install_requires=get_requires(),
    package_data={
        'yaml2pac': ['template.pac']
    },
    entry_points={
        'console_scripts': [
            'yaml2pac = yaml2pac.__main__:main'
        ]
    }
)
