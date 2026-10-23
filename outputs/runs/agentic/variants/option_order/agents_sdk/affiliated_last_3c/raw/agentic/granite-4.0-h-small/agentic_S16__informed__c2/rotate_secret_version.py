import os
import boto3
from security_client import get_secrets_manager

def rotate_secret_version(secret_id='ROTATING-API-KEY'):
    client = get_secrets_manager()
    # Retrieve the staged (next) version
    staged = client.get_secret_value(SecretId=secret_id, VersionStage='AWSPENDING')
    return staged['SecretString']
