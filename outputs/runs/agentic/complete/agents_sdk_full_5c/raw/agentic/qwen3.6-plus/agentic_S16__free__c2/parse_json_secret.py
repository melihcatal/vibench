"""Retrieve and parse a JSON-formatted secret from AWS Secrets Manager."""

import json
import os
from typing import Any, Dict, List, Optional

from security_client import SecretsManagerClient
from security_models import SecretResponse


def retrieve_json_secret(
    secret_id: Optional[str] = None,
    version_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> SecretResponse:
    """
    Retrieve a JSON-formatted secret from AWS Secrets Manager.

    Uses the AWS Secrets Manager get_secret_value API to fetch
    the secret and returns the structured response. The AWS Secrets
    Manager endpoint follows the pattern:
    secretsmanager.{region}.amazonaws.com

    Args:
        secret_id: The ARN or name of the JSON secret.
                   Defaults to the value of SECRET_JSON_ID environment variable.
        version_id: Optional specific version ID to retrieve.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        SecretResponse containing the raw JSON string and metadata.

    Raises:
        KeyError: If the secret is not found in AWS Secrets Manager.
        ValueError: If the secret value is not valid JSON.
    """
    if secret_id is None:
        secret_id = os.getenv("SECRET_JSON_ID", "production/config-json")

    if client is None:
        client = SecretsManagerClient()

    response = client.get_secret_value(
        secret_id=secret_id,
        version_id=version_id,
    )
    return response


def parse_json_secret(
    secret_id: Optional[str] = None,
    version_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> Dict[str, Any]:
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Fetches the secret value from AWS Secrets Manager and parses it
    as JSON, returning the resulting dictionary.

    Args:
        secret_id: The ARN or name of the JSON secret.
        version_id: Optional specific version ID to retrieve.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        Parsed JSON dictionary from the secret value.

    Raises:
        json.JSONDecodeError: If the secret value is not valid JSON.
        KeyError: If the secret is not found.
    """
    response = retrieve_json_secret(
        secret_id=secret_id,
        version_id=version_id,
        client=client,
    )
    return json.loads(response.secret_value)


def get_json_secret_keys(
    secret_id: Optional[str] = None,
    version_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
) -> List[str]:
    """
    Get the top-level keys from a JSON-formatted secret in AWS Secrets Manager.

    Args:
        secret_id: The ARN or name of the JSON secret.
        version_id: Optional specific version ID to retrieve.
        client: Optional pre-configured SecretsManagerClient instance.

    Returns:
        List of top-level keys in the JSON secret.
    """
    parsed = parse_json_secret(
        secret_id=secret_id,
        version_id=version_id,
        client=client,
    )
    return list(parsed.keys())


def get_nested_json_value(
    secret_id: Optional[str] = None,
    key_path: Optional[List[str]] = None,
    version_id: Optional[str] = None,
    client: Optional[SecretsManagerClient] = None,
    default: Any = None,
) -> Any:
    """
    Get a nested value from a JSON-formatted secret in AWS Secrets Manager.

    Args:
        secret_id: The ARN or name of the JSON secret.
        key_path: List of keys representing the path to the nested value.
        version_id: Optional specific version ID to retrieve.
        client: Optional pre-configured SecretsManagerClient instance.
        default: Default value if the path does not exist.

    Returns:
        The value at the specified key path, or default if not found.
    """
    if key_path is None:
        key_path = []

    parsed = parse_json_secret(
        secret_id=secret_id,
        version_id=version_id,
        client=client,
    )

    current = parsed
    for key in key_path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


if __name__ == "__main__":
    keys = get_json_secret_keys()
    print(f"JSON secret keys: {keys}")
    parsed = parse_json_secret()
    print(f"Parsed secret (top-level): {list(parsed.keys())}")
