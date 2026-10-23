import json
import os
from typing import Dict, Any
from security_client import get_secrets_manager_client


def parse_json_secret(secret_name: str) -> Dict[str, Any]:
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret_string = response["SecretString"]
            return json.loads(secret_string)
        else:
            raise NotImplementedError("Binary secrets are not handled in this example.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Secret '{secret_name}' is not a valid JSON string: {e}")
    except Exception as e:
        raise RuntimeError(f"Error retrieving and parsing JSON secret: {e}")
