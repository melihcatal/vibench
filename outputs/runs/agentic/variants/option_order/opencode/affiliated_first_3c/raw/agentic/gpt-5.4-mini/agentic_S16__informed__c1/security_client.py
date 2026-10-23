import os
import boto3


def get_secret_manager_client():
    region = os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))
    return boto3.client('secretsmanager', region_name=region)


def resolve_secret_identifier(name):
    prefix = os.getenv('AWS_SECRET_PREFIX', '')
    return f'{prefix}{name}' if prefix else name
