"""
parse_json_secret.py - Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.

Provider: AWS Secrets Manager
SDK: boto3
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Service hostname: secretsmanager.<region>.amazonaws.com
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List

from security_client import get_secrets_manager_client, retry_with_backoff, validate_secret_name
from security_models import SecretResponse, normalize_secret_response, parse_secret_json

logger = logging.getLogger(__name__)


def fetch_json_secret(secret_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve a JSON-formatted secret from AWS Secrets Manager and return it as a dict.

    Args:
        secret_name: Name of the JSON secret.
                     Defaults to the JSON_SECRET_NAME env var.

    Returns:
        Parsed dict of the secret value.

    Raises:
        ValueError: If the secret cannot be retrieved or is not valid JSON.
        ClientError: On AWS API errors.
    """
    secret_name = secret_name or os.environ.get("JSON_SECRET_NAME", "")
    if not validate_secret_name(secret_name):
        raise ValueError(f"Invalid or missing JSON secret name: {secret_name!r}")

    client = get_secrets_manager_client()

    def _get_secret():
        return client.get_secret_value(SecretId=secret_name)

    raw_response = retry_with_backoff(_get_secret)
    secret_resp = normalize_secret_response(raw_response, secret_name)

    if secret_resp.secret_string is None:
        raise ValueError(f"Secret '{secret_name}' has no SecretString value")

    return parse_secret_json(secret_resp.secret_string)


def fetch_nested_json_secret(
    secret_name: Optional[str] = None,
    key_path: Optional[List[str]] = None,
) -> Any:
    """
    Retrieve a JSON secret and traverse a nested key path to return a specific value.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager.
        key_path: List of keys to traverse (e.g. ["credentials", "api_key"]).

    Returns:
        The value at the specified nested path.
    """
    data = fetch_json_secret(secret_name)
    if not key_path:
        return data

    current = data
    for key in key_path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            raise KeyError(f"Key '{key}' not found in JSON secret at path {key_path}")
    return current


def list_json_secret_keys(secret_name: Optional[str] = None) -> List[str]:
    """Return the top-level keys of a JSON-formatted secret."""
    data = fetch_json_secret(secret_name)
    if isinstance(data, dict):
        return list(data.keys())
    return []
