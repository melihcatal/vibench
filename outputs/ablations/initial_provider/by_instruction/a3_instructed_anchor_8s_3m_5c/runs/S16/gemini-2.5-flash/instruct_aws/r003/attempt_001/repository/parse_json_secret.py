import os
import json
from typing import Dict, Any
from security_client import get_secrets_manager_client

def parse_json_secret(secret_name: str) -> Dict[str, Any]:
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.

    Returns:
        A dictionary containing the parsed JSON secret.

    Raises:
        ValueError: If the secret is not found or is not a valid JSON string.
        RuntimeError: For other errors during secret retrieval.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error retrieving secret '{secret_name}': {e}")

    if 'SecretString' in get_secret_value_response:
        secret_string = get_secret_value_response['SecretString']
        try:
            return json.loads(secret_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Secret '{secret_name}' is not a valid JSON string: {e}")
    else:
        raise ValueError(f"Secret '{secret_name}' does not contain a SecretString.")
