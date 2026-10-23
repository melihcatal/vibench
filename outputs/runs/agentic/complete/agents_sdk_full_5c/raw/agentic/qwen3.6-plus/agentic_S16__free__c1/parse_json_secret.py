"""
parse_json_secret.py - Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.

Uses boto3 to fetch a secret from secretsmanager.amazonaws.com and
parse its JSON contents into structured data with key extraction utilities.
"""

from __future__ import annotations

import json
import logging
from typing import Optional, Dict, Any, List

from security_client import get_secretsmanager_client, get_secret_value
from security_models import SecretResponse, describe_secret, parse_secret_value_as_json

logger = logging.getLogger(__name__)


def parse_json_secret(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.
        version_id: Specific version ID to retrieve.
        version_stage: Version stage to retrieve.
        region: AWS region override.

    Returns:
        Parsed JSON dict from the secret value.
    """
    client = get_secretsmanager_client(region_name=region)
    logger.info("Parsing JSON secret from AWS Secrets Manager: %s", secret_name)

    secret_value_resp = get_secret_value(
        client,
        secret_id=secret_name,
        version_id=version_id,
        version_stage=version_stage,
    )

    secret_value = secret_value_resp.get("SecretString", "")
    parsed = parse_secret_value_as_json(secret_value)

    if not parsed and secret_value:
        logger.warning("Secret %s does not contain valid JSON", secret_name)

    return parsed


def extract_keys(
    secret_name: str,
    keys: List[str],
    version_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract specific keys from a JSON secret.

    Args:
        secret_name: The name or ARN of the secret.
        keys: List of keys to extract.
        version_id: Specific version ID.
        region: AWS region override.

    Returns:
        Dict with only the requested keys.
    """
    parsed = parse_json_secret(secret_name, version_id=version_id, region=region)
    return {k: parsed.get(k) for k in keys if k in parsed}


def get_nested_value(
    secret_name: str,
    key_path: str,
    separator: str = ".",
    region: Optional[str] = None,
) -> Any:
    """
    Get a nested value from a JSON secret using dot-separated path.

    Args:
        secret_name: The name or ARN of the secret.
        key_path: Dot-separated path to the value.
        separator: Path separator character.
        region: AWS region override.

    Returns:
        The value at the key path, or None.
    """
    parsed = parse_json_secret(secret_name, region=region)
    keys = key_path.split(separator)
    current = parsed
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    secret_name = "production/config/service-a"
    parsed = parse_json_secret(secret_name)
    logger.info("Parsed %d keys from JSON secret", len(parsed))
    print(f"Secret keys: {list(parsed.keys())}")
