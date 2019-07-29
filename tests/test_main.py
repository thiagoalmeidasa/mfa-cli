# -*- coding: utf-8 -*-
"""

tests.main.py
~~~~~~~~~~~~~~~~~

This module is used to test mfacli commands
"""

import random
import string
from tempfile import mkstemp

# import pytest
from mfacli.mfa_cli import TOTP
from pyotp import random_base32

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


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


def generate_keyfile():
    """Generate a real keyfile with random keys

    :return: valid keyfile path
    :rtype: str
    """
    _, keyfile_path = mkstemp()
    print(keyfile_path)

    with open(keyfile_path, 'a+t') as keyfile:
        count = 0
        while count <= 4:
            service_name, secret_key = generate_service_key_pair()
            keyfile.writelines(service_name + ': ' + secret_key + '\n')
            count += 1
        keyfile.seek(0)
        # data = f.read()
    return keyfile_path


def test_list_keys():
    """Fail due a not found keyfile

    :return: keynames
    :rtype: list
    """
    keyfile = generate_keyfile()
    totp = TOTP(keyfile)
    assert len(totp.secret_keys) == 5
