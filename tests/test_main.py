# -*- coding: utf-8 -*-
"""

tests.main.py
~~~~~~~~~~~~~~~~~

This module is used to test mfacli commands
"""

import os
import random
import re
import string
import tempfile

from click.testing import CliRunner

import pytest
from mfacli import mfa_cli
from pyotp import random_base32

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


@pytest.fixture(scope="module")
def runner():
    """An method to run command line script in isolation and captures the
    output"""
    return CliRunner()


@pytest.fixture()
def cleandir():
    """Using the standard tempfile and pytest fixtures to
    run file dependent tests in an empty directory.
    """
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)


def generate_service_key_pair():
    """Generate random service name with a valid key

    :return: service_name, secret_key
    :rtype: tuple
    """
    service_name = ""
    for i in range(5):
        if i % 2 == 0:
            service_name += random.choice(CONSONANTS)
        else:
            service_name += random.choice(VOWELS)
    return service_name, random_base32()


# @pytest.mark.usefixtures("cleandir")
# def test_cwd_again_starts_empty():
    # assert os.listdir(os.getcwd()) == []

@pytest.mark.usefixtures("cleandir")
def generate_keyfile():
    """Generate a real keyfile with random keys

    :return: valid keyfile path
    :rtype: str
    """
    _, keyfile_path = tempfile.mkstemp(dir=os.getcwd())

    with open(keyfile_path, 'a+t') as keyfile:
        count = 0
        while count <= 4:
            service_name, secret_key = generate_service_key_pair()
            keyfile.writelines(service_name + ': ' + secret_key + '\n')
            count += 1
        keyfile.seek(0)
        # data = f.read()
    return keyfile_path


@pytest.mark.usefixtures("cleandir")
def test_list_keys():
    """List keys given a valid keyfile """

    keyfile = generate_keyfile()
    totp = mfa_cli.TOTP(keyfile)
    assert len(totp.secret_keys) == 5


@pytest.mark.usefixtures("runner", "cleandir")
def test_list_keys_cli(runner):
    """List keys given a valid keyfile as cli arg """

    keyfile = generate_keyfile()
    result = runner.invoke(mfa_cli.main, ['list-keys', '--keyfile', keyfile])
    assert result.exit_code == 0
    assert result.output.count('\n') == 5


@pytest.mark.usefixtures("runner", "cleandir")
def test_fail_keyfile_not_found_cli(runner):
    """Fail due a not found keyfile"""

    keyfile = r"/tmp" + random_base32()
    result = runner.invoke(mfa_cli.main, ['list-keys', '--keyfile', keyfile])
    assert result.exit_code == 2
    assert result.output.find("does not exist")


@pytest.mark.usefixtures("runner", "cleandir")
def test_new_totp_prompt_keyname_cli(runner):
    """Get a valid otp by prompting service name on cli """

    expected_result_regex = r"\w+\s\w+\:\s\d{6}\n\w+\s\w+\:\s\d{,2}\s\w+"
    regexp = re.compile(expected_result_regex)
    keyfile = generate_keyfile()
    for random_key_number in range(0, 5):
        result = runner.invoke(mfa_cli.main,
                               ['new-totp', '--keyfile', keyfile],
                               input='{}\n'.format(random_key_number))
        assert result.exit_code == 0
        assert regexp.search(result.output) != -1


@pytest.mark.usefixtures("runner", "cleandir")
def test_new_totp_prompt_keyname_out_of_range_cli(runner):
    """Fail due an out of range keynumber"""

    expected_result_string = r"Choice out of range. Start again"
    keyfile = generate_keyfile()
    for key_number in (-1, 6):
        result = runner.invoke(mfa_cli.main,
                               ['new-totp', '--keyfile', keyfile],
                               input='{}\n'.format(key_number))
        assert result.exit_code == 1
        assert result.output.find(expected_result_string) != -1


@pytest.mark.usefixtures("runner", "cleandir")
def test_fail_new_totp_invalid_keyname_cli(runner):
    """Fail due an invalid keyname"""

    expected_result_string = r"Key not in your keyfiles, try to list your keys"
    keyfile = generate_keyfile()
    result = runner.invoke(mfa_cli.main, [
        'new-totp', '--keyfile', keyfile, '--keyname', '{}'.format(
            random_base32())
    ])
    assert result.exit_code == 1
    assert result.output.find(expected_result_string) != -1


@pytest.mark.usefixtures("runner", "cleandir")
def test_fail_new_totp_invalid_keyformat_cli(runner):
    """Fail due an invalid keyname"""

    expected_result_string = "Invalid key for: {} verify it with your provider \
                             or get a new one".format(service_name)
    keyfile = generate_keyfile()
    totp = mfa_cli.TOTP(keyfile)
    totp.secret_keys
    result = runner.invoke(mfa_cli.main, [
        'new-totp', '--keyfile', keyfile, '--keyname', '{}'.format(
            random_base32())
    ])
    assert result.exit_code == 1
    assert result.output.find(expected_result_string) != -1
