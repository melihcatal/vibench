import os
import boto3
from security_models import SecretConfig
from security_client import load_provider_env
from typing import Optional

def fetch_api_key(secret_name: Optional[str] = None) -> str:
    provider = 'aws'
    load_provider_env(provider)
    config = SecretConfig(name=secret_name or os.getenv('SECRET_NAME', 'api-key'))
    client = boto3.client(
        'secretsmanager',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    response = client.get_secret_value(SecretId=config.name)
    return response['SecretString']