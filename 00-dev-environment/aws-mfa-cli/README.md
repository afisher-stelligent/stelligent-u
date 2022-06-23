# AWS MFA Generator for CLI

This Python 3 script allows Mac or Linux users to generate 8 hour sessions using MFA.

## Prerequistes

Follow the instructions provided in Lab 0.1.1: AWS Access Keys before continuing. Add the following line to your ~/.aws/config file's [default] section before continuing:

`mfa_serial = arn:aws:iam::<your MFA Serial ARN>`

## Installation

Clone the repository, CD to this directory, and then do a `pip3 install`:

    `pip3 install -r requirements.txt`

This will install the Boto3 library and all it's dependencies.

## Running the script

To run the script, execute as follows:

`python3 aws-mfa.py`

and follow the prompts. This will create a new profile called `temp` which you can either add to your `.bashrc` or `.zshrc` file as an environment variable or use with the `--profile` flag with the aws cli commands.
