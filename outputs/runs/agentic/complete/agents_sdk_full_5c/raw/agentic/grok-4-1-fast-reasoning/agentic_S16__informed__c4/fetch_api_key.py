import boto3
import os
from security_client import get_aws_region

def fetch_api_key(secret_name: str) -> str:
    region = get_aws_region()
    client = boto3.client(
        'secretsmanager',
        region_name=region
    )
    response = client.get_secret_value(SecretId=secret_name)
    if 'SecretString' in response:
        return response['SecretString']
    else:
        return bytes(response['SecretBinary']).decode()
