
import boto3
import botocore
import configparser
import os
import re

if __name__ == '__main__':
    # read in OTP
    mfa_totp = input('Enter the code from your registered MFA device: ')

    # validate input
    if not re.match(r'^[0-9]{6}$', mfa_totp):  # assumes 6-digit MFA code
        print(f'{mfa_totp} is not a valid MFA Code!')
        exit(1)

    # read in the AWS CLI config file and find the MFA serial number
    aws_config = configparser.RawConfigParser()
    config_path = os.path.join(os.path.expanduser('~'), '.aws/config')
    aws_config.read(config_path)
    mfa_serial = aws_config.get('default', 'mfa_serial')

    try:
        # set the default profile name to the default profile...
        # if the profile is set to something that uses a session token in the environment
        # variables, this script will fail.
        boto3.setup_default_session(profile_name='default')
        client = boto3.client('sts')
        response = client.get_session_token(DurationSeconds=28800, SerialNumber=mfa_serial, TokenCode=mfa_totp)
    except botocore.exceptions.ClientError as error:
        print('An error occured aquiring credentials')
        print(error)
        exit(1)

    # get the bits we need to form a temporary profile
    creds = response.get('Credentials')
    session_token = creds.get('SessionToken')
    expiry = creds.get('Expiration').ctime()

    # load in configuration file
    credentials = configparser.RawConfigParser()
    path = os.path.join(os.path.expanduser('~'), '.aws/credentials')
    credentials.read(path)

    # check to see if the [temp] section exists, if not, create it
    if not credentials.has_section('temp'):
        credentials.add_section('temp')

    # update the [temp] section with the correct values
    credentials['temp']['aws_access_key_id'] = creds.get('AccessKeyId')
    credentials['temp']['aws_secret_access_key'] = creds.get('SecretAccessKey')
    credentials['temp']['aws_session_token'] = creds.get('SessionToken')

    # write out credentials file
    with open(path, 'w') as credentials_file:
        credentials.write(credentials_file)

    print(f'Session successfully established for the AWS CLI. \n\nYour session will expire at {expiry}. \nIt is recommended to add export AWS_PROFILE=temp to your .bashrc or .zshrc for ease of use. Otherwise, use the --profile flag to use these credentials with the AWS CLI')
