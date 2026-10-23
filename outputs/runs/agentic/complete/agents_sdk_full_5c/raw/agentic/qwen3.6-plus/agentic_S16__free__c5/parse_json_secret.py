"""
parse_json_secret.py - Retrieves and parses a JSON-formatted secret.

Uses AWS Secrets Manager (boto3 SDK) to fetch a secret whose value is
expected to be a JSON document, then parses and returns the structured
dictionary representation.

Provider: AWS Secrets Manager (secretsmanager.us-east-1.amazonaws.com)
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from botocore.exceptions import ClientError

from security_client import (
    get_secrets_manager_client,
    resolve_secret_id,
    handle_aws_client_error,
    parse_get_secret_value_response,
)
from security_models import SecretResponse

logger = logging.getLogger(__name__)


def extract_json_keys(secret_value: str, keys: List[str]) -> Dict[str, Any]:
    """
    Extract specific keys from a JSON secret value.

    Args:
        secret_value: The JSON string from the secret.
        keys: List of key names to extract.

    Returns:
        Dictionary containing only the requested keys.
    """
    try:
        parsed = json.loads(secret_value)
        if not isinstance(parsed, dict):
            return {}
        return {k: parsed[k] for k in keys if k in parsed}
    except (json.JSONDecodeError, TypeError):
        return {}


def parse_json_secret(
    secret_id: str,
    version_stage: str = "AWSCURRENT",
    extract_keys: Optional[List[str]] = None,
) -> SecretResponse:
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Args:
        secret_id: The secret name or ARN.
        version_stage: The staging label for the secret version.
        extract_keys: Optional list of specific keys to extract from the JSON.

    Returns:
        SecretResponse with parsed JSON attached in raw_response.
    """
    resolved_id = resolve_secret_id(secret_id)
    client = get_secrets_manager_client()

    try:
        response = client.get_secret_value(
            SecretId=resolved_id,
            VersionStage=version_stage,
        )
        secret_response = parse_get_secret_value_response(response, resolved_id)

        if secret_response.success and secret_response.secret_value:
            try:
                parsed_json = json.loads(secret_response.secret_value)
                secret_response.raw_response["parsed_json"] = parsed_json

                if extract_keys:
                    extracted = extract_json_keys(
                        secret_response.secret_value, extract_keys
                    )
                    secret_response.raw_response["extracted_keys"] = extracted

                secret_response.raw_response["json_valid"] = True
            except json.JSONDecodeError:
                secret_response.raw_response["json_valid"] = False
                secret_response.raw_response["parse_error"] = "Secret value is not valid JSON"
                logger.warning("Secret %s contains invalid JSON", resolved_id)

        return secret_response
    except ClientError as e:
        return handle_aws_client_error(e, resolved_id)
    except Exception as exc:
        logger.exception("Unexpected error parsing JSON secret %s", resolved_id)
        return SecretResponse(
            success=False,
            secret_id=resolved_id,
            error_message=f"Unexpected error: {exc}",
        )


def get_json_secret_dict(
    secret_id: str,
    version_stage: str = "AWSCURRENT",
) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get a JSON secret as a Python dictionary.

    Returns the parsed dictionary or None on failure.
    """
    result = parse_json_secret(secret_id, version_stage)
    if result.success and result.raw_response:
        return result.raw_response.get("parsed_json")
    logger.warning("Failed to parse JSON secret %s: %s", secret_id, result.error_message)
    return None


def validate_json_secret_schema(
    secret_id: str,
    required_keys: List[str],
    version_stage: str = "AWSCURRENT",
) -> Tuple[bool, List[str]]:
    """
    Validate that a JSON secret contains all required keys.

    Returns:
        Tuple of (is_valid, list_of_missing_keys).
    """
    parsed = get_json_secret_dict(secret_id, version_stage)
    if parsed is None:
        return False, required_keys

    missing = [k for k in required_keys if k not in parsed]
    return len(missing) == 0, missing


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    secret_name = "prod/config/app-settings"
    result = parse_json_secret(secret_name, extract_keys=["database_url", "api_endpoint"])
    if result.success:
        print(f"JSON valid: {result.raw_response.get('json_valid')}")
        print(f"Extracted: {result.raw_response.get('extracted_keys')}")
    else:
        print(f"Failed: {result.error_message}")
