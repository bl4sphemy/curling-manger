#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='curling-manger',
    version='1.0.0',
    author='Brian Rawlins',
    author_email='brp0010@auburn.edu',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['PyQt5', 'PyQT5-tools', 'yagmail'],
    packages=[
        'app',
        'qt_windows',
        'module6',
    ],
)
