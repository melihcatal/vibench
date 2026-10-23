import os
import json
from security_client import get_secrets_manager_client

def fetch_db_secret(secret_name: str) -> dict:
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        elif 'SecretBinary' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretBinary'].decode('utf-8'))
    except Exception:
        raise
    return {}
