"""
Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.

Fetches a secret whose value is a JSON payload, parses it into a structured
dictionary, and provides utilities to access nested fields safely.

Provider: AWS Secrets Manager
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
import json
from typing import Optional, Dict, Any, List

from security_client import create_secrets_manager_client, handle_secrets_error, normalize_secret_response
from security_models import (
    SecretRequest,
    ParsedSecret,
    parse_secret_json,
    normalize_aws_response_to_secret_response,
    build_error_secret_response,
)


def parse_json_secret(
    secret_name: str,
    region: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
) -> Dict[str, Any]:
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret containing JSON data.
        region: Optional AWS region override.
        version_stage: Version stage to retrieve (default: AWSCURRENT).

    Returns:
        Dictionary with parsed JSON data and metadata.
    """
    try:
        client = create_secrets_manager_client(region=region)

        response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage,
        )

        secret_string = response.get("SecretString", "")
        if not secret_string:
            return {
                "success": False,
                "secret_id": secret_name,
                "error_code": "EMPTY_SECRET",
                "error_message": "Secret value is empty or binary-only.",
            }

        parsed = parse_secret_json(secret_string)
        if not parsed.is_valid:
            return {
                "success": False,
                "secret_id": secret_name,
                "error_code": "PARSE_ERROR",
                "error_message": parsed.parse_error or "Failed to parse JSON secret",
                "raw_value_length": len(secret_string),
            }

        result = {
            "success": True,
            "secret_id": response.get("Name", secret_name),
            "arn": response.get("ARN", ""),
            "version_id": response.get("VersionId", ""),
            "version_stage": version_stage,
            "parsed_data": parsed.parsed_data,
            "key_count": len(parsed.parsed_data) if isinstance(parsed.parsed_data, dict) else 0,
            "created_date": response.get("CreatedDate"),
        }
        return result

    except Exception as e:
        if hasattr(e, "response") and "Error" in e.response:
            error_info = handle_secrets_error(e)
            return {
                "success": False,
                "secret_id": secret_name,
                "error_code": error_info.get("error_code", ""),
                "error_message": error_info.get("error_message", str(e)),
                "request_id": error_info.get("request_id", ""),
            }
        return {
            "success": False,
            "secret_id": secret_name,
            "error_code": "CLIENT_ERROR",
            "error_message": str(e),
        }


def get_nested_secret_field(
    secret_name: str,
    key_path: str,
    default: Any = None,
    region: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
) -> Any:
    """
    Retrieve a specific nested field from a JSON secret using dot notation.

    Args:
        secret_name: The name or ARN of the secret.
        key_path: Dot-separated path to the desired field (e.g., 'database.host').
        default: Default value if the key path is not found.
        region: Optional AWS region override.
        version_stage: Version stage to retrieve.

    Returns:
        The value at the key path, or the default value.
    """
    result = parse_json_secret(secret_name, region=region, version_stage=version_stage)
    if not result.get("success"):
        return default

    parsed_data = result.get("parsed_data", {})
    keys = key_path.split(".")
    current = parsed_data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current


def extract_secret_keys(
    secret_name: str,
    region: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
) -> List[str]:
    """
    Extract all top-level keys from a JSON secret.

    Args:
        secret_name: The name or ARN of the secret.
        region: Optional AWS region override.
        version_stage: Version stage to retrieve.

    Returns:
        List of top-level keys in the parsed JSON secret.
    """
    result = parse_json_secret(secret_name, region=region, version_stage=version_stage)
    if not result.get("success"):
        return []

    parsed_data = result.get("parsed_data", {})
    if isinstance(parsed_data, dict):
        return list(parsed_data.keys())
    return []
