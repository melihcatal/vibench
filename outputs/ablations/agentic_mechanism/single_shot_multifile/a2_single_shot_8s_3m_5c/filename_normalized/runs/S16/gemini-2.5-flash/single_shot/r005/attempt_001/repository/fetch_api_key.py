import os
from security_client import get_secrets_manager_client

def fetch_api_key(secret_name: str) -> str:
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        elif 'SecretBinary' in get_secret_value_response:
            return get_secret_value_response['SecretBinary'].decode('utf-8')
    except Exception:
        raise
    return ""
