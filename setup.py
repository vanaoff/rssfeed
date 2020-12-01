#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="rssfeed",
    description="Morgan Dejavu service",
    author_email="ivan.heda@gmail.com",
    license="MIT",
    packages=find_packages(include=["rssfeed*"]),
    install_requires=["flask"],
)
