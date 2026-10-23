import json
from typing import Dict, Any
from security_client import get_secrets_manager_client

def get_parsed_json_secret(secret_name: str) -> Dict[str, Any]:
    """
    Retrieves a secret from AWS Secrets Manager and parses it as JSON.

    Args:
        secret_name: The name or ARN of the secret.

    Returns:
        A dictionary containing the secret data.
    """
    client = get_secrets_manager_client()
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    
    secret = get_secret_value_response['SecretString']
    parsed_secret = json.loads(secret)
    
    return parsed_secret
