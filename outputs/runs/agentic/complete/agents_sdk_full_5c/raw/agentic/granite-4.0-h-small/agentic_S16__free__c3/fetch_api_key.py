# fetch_api_key.py
import os
import json
from security_client import get_secret_manager_client

def fetch_api_key(secret_name: str) -> str:
    """Fetch an API key stored as a secret value.

    Uses AWS Secrets Manager as the concrete provider.
    """
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']
    secret_json = json.loads(secret_string)
    return secret_json.get('api_key')
