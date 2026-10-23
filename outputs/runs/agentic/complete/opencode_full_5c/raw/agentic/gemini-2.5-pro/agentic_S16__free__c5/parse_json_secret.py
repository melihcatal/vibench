import json
import os
from typing import Any, Dict
from security_client import get_aws_secrets_manager_client


def parse_json_secret(secret_name: str) -> Dict[str, Any] | None:
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        return None

    secret_string = get_secret_value_response.get("SecretString")
    if not secret_string:
        return None

    try:
        return json.loads(secret_string)
    except json.JSONDecodeError:
        return None
