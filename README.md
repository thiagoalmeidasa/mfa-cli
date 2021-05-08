# mfa-cli

[![CI](https://github.com/thiagoalmeidasa/mfa-cli/actions/workflows/ci.yaml/badge.svg)](https://github.com/thiagoalmeidasa/mfa-cli/actions/workflows/ci.yaml)

CLI tool for generating one-time passwords.

## Usage

```bash
$ python -m mfa_cli list-keys --keyfile codes.yml
$ python -m mfa_cli new-totp --keyfile codes.yml
$ python -m mfa_cli new-totp --keyfile codes.yml --keyname myservice
```

## Instalation

```bash
pip install mfa-cli
```
