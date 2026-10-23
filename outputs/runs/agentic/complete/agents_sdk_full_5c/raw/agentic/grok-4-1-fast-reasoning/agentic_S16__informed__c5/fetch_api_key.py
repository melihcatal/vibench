import boto3
import os
from security_client import parse_api_key_secret
from security_models import ApiKeySecret

def fetch_api_key(secret_id: str = None) -> ApiKeySecret:
    if secret_id is None:
        secret_id = os.getenv('API_KEY_SECRET_ID', 'prod/api-key')
    client = boto3.client(
        'secretsmanager',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    response = client.get_secret_value(SecretId=secret_id)
    secret_str = response['SecretString']
    return parse_api_key_secret(secret_str)