#!/usr/bin/env python
# encoding: utf-8
"""
setup.py
"""

from setuptools import setup, find_packages
import os

execfile(os.path.join('src', 'followall', 'version.py'))

setup(
    name = 'followall',
    version = VERSION,
    description = 'followall allows you to follow everyone Twitter suggests.',
    author = 'Kurtiss Hare',
    author_email = 'kurtiss@gmail.com',
    url = 'http://www.github.com/kurtiss/followall',
    packages = find_packages('src'),
    package_dir = {'' : 'src'},
    install_requires = ['tweepy>=1.7.1'],
    scripts = ['bin/followall'],
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe = False
)
