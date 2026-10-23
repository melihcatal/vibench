import json
import os
from security_client import get_secrets_manager_client

def retrieve_and_parse_json_secret(secret_name: str) -> dict:
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            secret_string = get_secret_value_response['SecretString']
            return json.loads(secret_string)
        elif 'SecretBinary' in get_secret_value_response:
            secret_binary = get_secret_value_response['SecretBinary']
            return json.loads(secret_binary.decode('utf-8'))
    except json.JSONDecodeError as e:
        raise ValueError(f"Secret '{secret_name}' is not valid JSON.") from e
    except Exception:
        raise
    return {}
