import boto3
import os
from typing import Dict, Any

from security_client import get_secrets_config

def fetch_api_key(secret_id: str) -> str:
    config = get_secrets_config()
    client = boto3.client(
        'secretsmanager',
        region_name=config['aws_region']
    )
    response = client.get_secret_value(SecretId=secret_id)
    return response['SecretString']