import json
import os
from typing import Dict, Any
from security_client import AWSSecretManagerClient
from security_models import SecretData


def parse_json_secret(secret_name: str) -> Dict[str, Any]:
    """Retrieves and parses a JSON-formatted secret from AWS Secrets Manager."""
    client = AWSSecretManagerClient()
    try:
        get_secret_value_response = client.client.get_secret_value(SecretId=secret_name)
        if "SecretString" in get_secret_value_response:
            secret_string = get_secret_value_response["SecretString"]
            secret_data = SecretData(secret_string)
            return secret_data.to_json()
        else:
            raise ValueError("SecretString not found in response.")
    except Exception as e:
        print(f"Error fetching and parsing JSON secret: {e}")
        raise
