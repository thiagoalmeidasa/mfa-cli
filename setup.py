# -*- coding: utf-8 -*-
"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search('^__version__\s*=\s*"(.*)"',
                    open('mfacli/mfa_cli.py').read(), re.M).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="mfa-cli",
    packages=["mfacli"],
    entry_points={"console_scripts": ['mfa-cli = mfacli.mfa_cli:main']},
    version=version,
    description='CLI tool for generating one-time passwords.',
    long_description=long_descr,
    author='Thiago Almeida',
    author_email='thiagoalmeidasa@gmail.com',
    url='https://github.com/thiagoalmeidasa/mfa-cli',
    install_requires=['pyotp', 'pyyaml', 'click', 'pyaescrypt'],
    tests_require=['pylint'],
)
