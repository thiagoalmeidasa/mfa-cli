# -*- coding: utf-8 -*-
"""setup.py: setuptools control."""

from setuptools import setup

with open("README.md", "rb") as f:
    LONG_DESCR = f.read().decode("utf-8")

setup(
    name="mfa-cli",
    packages=["mfacli"],
    entry_points={"console_scripts": ['mfa-cli = mfacli.mfa_cli:main']},
    version_config=True,
    setup_requires=['setuptools-git-versioning'],
    description='CLI tool for generating one-time passwords.',
    long_description=LONG_DESCR,
    author='Thiago Almeida',
    author_email='thiagoalmeidasa@gmail.com',
    url='https://github.com/thiagoalmeidasa/mfa-cli',
    install_requires=[
        'pyotp==2.6.0', 'pyyaml==5.4', 'click==7.1', 'pyaescrypt==5.0.0',
        'pyperclip==1.8.2'
    ],
    tests_require=['pylint'],
)
