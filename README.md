# mfa-cli

[![CI](https://github.com/thiagoalmeidasa/mfa-cli/actions/workflows/ci.yaml/badge.svg)](https://github.com/thiagoalmeidasa/mfa-cli/actions/workflows/ci.yaml)

CLI tool for generating one-time passwords.

## Instalation

```bash
pip install mfa-cli
```

## Usage

```bash
$ mfa-cli list-keys --keyfile codes.yml
$ mfa-cli new-totp --keyfile codes.yml
$ mfa-cli new-totp --keyfile codes.yml --keyname myservice
```
