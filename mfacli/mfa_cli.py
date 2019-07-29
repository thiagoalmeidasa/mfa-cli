# -*- coding: utf-8 -*-
"""Cli entrypoint for mfa_cli

This modules use click (https://click.palletsprojects.com/en/7.x/) to manage
cli args for mfa_cli.

Example:
    $ python -m mfa_cli list-keys --keyfile codes.yml
    $ python -m mfa_cli new-totp --keyfile codes.yml
    $ python -m mfa_cli new-totp --keyfile codes.yml --keyname myservice

Todo:
    * Use pyAesCrypt for keyfile encryption
"""

__version__ = "0.2.0"

from datetime import datetime

from .manage_totp import TOTP

try:
    import click
except ImportError:
    print("You must install click:")
    print("pip install click")

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# yapf: disable
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def main():
    """CLI tool for generating one-time passwords."""


# yapf: enable
@main.command()
@click.option('-kf',
              '--keyfile',
              type=click.Path(exists=True),
              required=True,
              help='YAML file with service keys')
@click.option('-kn', '--keyname', help='keyname to generate a new totp')
def new_totp(keyname, keyfile):
    """Generate a new key based totp for a service"""
    totp = TOTP(keyfile)
    totp_now = totp.get_new_totp(keyname)
    remaining_time = 30 - (datetime.now().second % 30)
    print(
        "Your totp for {} service:\n {}\n It is valid for {} seconds.".format(
            keyname, totp_now, remaining_time))


@main.command()
@click.option('-kf',
              '--keyfile',
              type=click.Path(exists=True),
              required=True,
              help='YAML file with service keys')
def list_keys(keyfile):
    """
    List all keys from a key file


    Parameters:
        keyfile: path to file containing all service keys
    """
    totp = TOTP(keyfile)
    totp.list_keys()


if __name__ == '__main__':
    main()
