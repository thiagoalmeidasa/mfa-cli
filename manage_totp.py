#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate totp and list services
"""
import sys

import yaml

try:
    import pyotp
except ImportError:
    print("You must install pyotp:")
    print("pip install pyotp")


class TOTP:
    """
    Read encrypted file containing all secret keys
    Parameters:
        keyfile: path to keyfile
    """
    def __init__(self, keyfile):
        self.keyfile = keyfile
        self.secret_keys = self.read_keys_file()

    def read_keys_file(self):
        """
        Read encrypted file containing all secret keys
        Parameters:
            keyfile: path to file containing all service keys
        """
        with open(self.keyfile, 'r') as content_stream:
            try:
                self.secret_keys = yaml.safe_load(content_stream)
                return self.secret_keys
            except yaml.scanner.ScannerError as yse:
                print("Invalid keyfile: {}".format(yse))
                sys.exit(1)

    def list_keys(self):
        """
        Read encrypted file and list keys
        Returns:        None
        Return type:    str
        """
        for key in self.secret_keys:
            print(key)
        return 0

    def choose_one_key(self):
        """
        Set a valid key from the keys list
        Returns:        keyname
        Return type:    str
        """
        for ele in enumerate(self.secret_keys):
            print("{} - {}".format(ele[0], ele[1]))
        try:
            keynumber = int(input("Enter a key number: "))
        except ValueError:
            print("You must select a key number.")
            sys.exit(1)
        if 0 <= keynumber <= len(self.secret_keys) - 1:
            chosen_key = list(self.secret_keys)[keynumber]
            return chosen_key
        print("Choice out of range. Start again")
        sys.exit(1)

    def get_key_by_name(self, keyname):
        """
        Get secret keys filtering by name
        Parameters:
            keyname: name of desired key
        Returns:  secret key for a service
        Return type:	str
        """
        return self.secret_keys[keyname]

    def get_new_totp(self, keyname=''):
        """
        Generate the current time OTP for a service(keyname)
        Parameters:
            keyname: service keyname to generate a totp

        Returns:	OTP value
        Return type:	str
        """
        if not self.secret_keys:
            self.read_keys_file()

        if not keyname:
            print("No key selected, select a key from the list:")
            keyname = self.choose_one_key()

        if keyname in self.secret_keys.keys():
            return pyotp.TOTP(self.get_key_by_name(keyname)).now()

        print("Invalid key, try to list your keys")
        sys.exit(1)
