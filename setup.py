# -*- coding: UTF-8 -*-
from setuptools import find_packages, setup

import codecs
import os

_version = "2.0.0"
_packages = find_packages('.', exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

if os.path.exists('README.rst'):
    _long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    _long_description = ""

setup(
    name='django-laterpay',
    version=_version,

    description="LaterPay Django tools",
    long_description=_long_description,
    author="LaterPay GmbH",
    author_email="support@laterpay.net",
    url="https://github.com/laterpay/django-laterpay",
    license='MIT',
    keywords="LaterPay API client Django",

    test_suite="tests",

    packages=_packages,

    install_requires=(
        'laterpay-client>=4.1',
        'Django>=1.8',
    ),

    classifiers=(
        # "Development Status :: 3 - Alpha",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
