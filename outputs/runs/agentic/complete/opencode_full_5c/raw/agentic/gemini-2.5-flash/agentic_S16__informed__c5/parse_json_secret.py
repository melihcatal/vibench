import os
import json
from typing import Optional, Dict, Any
from security_client import get_secrets_manager_client
from security_models import JsonSecret


def parse_json_secret(
    secret_name: str, version_stage: str = "AWSCURRENT"
) -> Optional[JsonSecret]:
    """Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret to retrieve.
        version_stage: The version stage of the secret to retrieve (e.g., 'AWSCURRENT').

    Returns:
        A JsonSecret object containing the parsed JSON data, or None if not found or malformed.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name, VersionStage=version_stage
        )
        if "SecretString" in get_secret_value_response:
            secret_string = get_secret_value_response["SecretString"]
            json_data = json.loads(secret_string)
            return JsonSecret(
                name=secret_name,
                json_data=json_data,
                version_id=get_secret_value_response.get("VersionId"),
            )
        else:
            print(f"Secret '{secret_name}' did not contain a SecretString.")
            return None
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Secret '{secret_name}' content is not valid JSON.")
        return None
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        return None
