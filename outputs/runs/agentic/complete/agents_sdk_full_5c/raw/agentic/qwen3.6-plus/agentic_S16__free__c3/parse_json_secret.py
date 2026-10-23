"""
Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

This module fetches secrets stored as JSON and parses them into
structured Python dictionaries for application use.
"""

import json
import logging
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from security_client import get_secrets_manager_client
from security_models import SecretFetchResult

logger = logging.getLogger(__name__)

AWS_PROVIDER_ID = "aws-secrets-manager"
AWS_SECRETSMANAGER_REGION = "us-east-1"


def parse_json_secret(
    secret_name: str, region_name: str = "us-east-1"
) -> SecretFetchResult:
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the JSON secret.
        region_name: AWS region for Secrets Manager.

    Returns:
        SecretFetchResult with parsed JSON data in secret_data field.
    """
    try:
        client = get_secrets_manager_client(region_name=region_name)

        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response.get("SecretString")

        if not secret_string:
            return SecretFetchResult(
                success=False,
                secret_name=secret_name,
                provider=AWS_PROVIDER_ID,
                error="Secret contains no string value",
            )

        parsed_data = json.loads(secret_string)

        return SecretFetchResult(
            success=True,
            secret_name=secret_name,
            secret_value=secret_string,
            secret_data=parsed_data,
            version_id=response.get("VersionId"),
            arn=response.get("ARN"),
            provider=AWS_PROVIDER_ID,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        logger.error(
            "AWS Secrets Manager error parsing JSON secret %s: %s",
            secret_name,
            error_code,
        )
        return SecretFetchResult(
            success=False,
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            error=f"AWS error: {error_code}",
        )
    except json.JSONDecodeError as e:
        return SecretFetchResult(
            success=False,
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            error=f"Invalid JSON in secret: {str(e)}",
        )


def get_secret_keys(
    secret_name: str, region_name: str = "us-east-1"
) -> List[str]:
    """
    Get the top-level keys from a JSON-formatted AWS secret.

    Args:
        secret_name: The secret name or ARN.
        region_name: AWS region.

    Returns:
        List of top-level key names from the parsed JSON secret.
    """
    result = parse_json_secret(secret_name, region_name)
    if result.success and result.secret_data and isinstance(result.secret_data, dict):
        return list(result.secret_data.keys())
    return []


def get_nested_value(
    secret_name: str, key_path: str, region_name: str = "us-east-1"
) -> Optional[Any]:
    """
    Get a nested value from a JSON secret using dot-notation key path.

    Args:
        secret_name: The secret name or ARN.
        key_path: Dot-separated path to the desired value (e.g., 'database.host').
        region_name: AWS region.

    Returns:
        The nested value or None if not found.
    """
    result = parse_json_secret(secret_name, region_name)
    if not result.success or not result.secret_data:
        return None

    keys = key_path.split(".")
    current = result.secret_data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current
