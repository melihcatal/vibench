import boto3
from typing import Dict, Any
from security_client import get_aws_config

def fetch_api_key(secret_id: str) -> str:
    config = get_aws_config()
    client = boto3.client('secretsmanager', **config)
    response = client.get_secret_value(SecretId=secret_id)
    return response['SecretString']
