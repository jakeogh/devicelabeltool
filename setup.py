# -*- coding: utf-8 -*-

import fastentrypoints
from setuptools import find_packages, setup

dependencies = ["click"]

config = {
    "version": "0.1",
    "name": "devicelabeltool",
    "url": "https://github.com/jakeogh/devicelabeltool",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "create or modify device (disk) label",
    "long_description": __doc__,
    "packages": find_packages(exclude=['tests']),
    "package_data": {"devicelabeltool": ['py.typed']},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
    "entry_points": {
        "console_scripts": [
            "devicelabeltool=devicelabeltool.devicelabeltool:cli",
        ],
    },
}

setup(**config)