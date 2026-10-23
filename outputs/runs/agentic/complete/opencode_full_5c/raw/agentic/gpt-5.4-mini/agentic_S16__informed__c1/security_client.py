import os
import boto3


def get_secret_client(provider='aws'):
    if provider == 'aws':
        return boto3.client('secretsmanager')
    raise ValueError('unsupported provider')


def get_secret_name(env_name, default):
    return os.environ.get(env_name, default)
