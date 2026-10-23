"""
Fetches an API key from AWS Secrets Manager.

Retrieves a named API key secret from the AWS Secrets Manager service
using the boto3 SDK. Returns the secret value along with version metadata.

Provider: AWS Secrets Manager
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
from typing import Optional, Dict, Any

from security_client import create_secrets_manager_client, handle_secrets_error, normalize_secret_response
from security_models import SecretResponse, normalize_aws_response_to_secret_response, build_error_secret_response


def fetch_api_key(
    secret_name: str,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch an API key secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret containing the API key.
        region: Optional AWS region override.

    Returns:
        Dictionary with the API key value and metadata, or error details.
    """
    try:
        client = create_secrets_manager_client(region=region)

        response = client.get_secret_value(SecretId=secret_name)

        normalized = normalize_secret_response(response)

        secret_value = normalized.get("secret_string", "")
        if not secret_value and "secret_binary" in normalized:
            secret_value = normalized["secret_binary"].decode("utf-8", errors="replace")

        result = {
            "success": True,
            "secret_id": normalized.get("name", secret_name),
            "arn": normalized.get("arn", ""),
            "version_id": normalized.get("version_id", ""),
            "version_stages": normalized.get("version_stage", []),
            "api_key": secret_value,
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


def fetch_api_key_with_version(
    secret_name: str,
    version_stage: str = "AWSCURRENT",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetch an API key from AWS Secrets Manager at a specific version stage.

    Args:
        secret_name: The name or ARN of the secret.
        version_stage: The version stage to retrieve (e.g., AWSCURRENT, AWSPENDING).
        region: Optional AWS region override.

    Returns:
        Dictionary with the API key value and version metadata.
    """
    try:
        client = create_secrets_manager_client(region=region)

        response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage,
        )

        normalized = normalize_secret_response(response)

        secret_value = normalized.get("secret_string", "")
        if not secret_value and "secret_binary" in normalized:
            secret_value = normalized["secret_binary"].decode("utf-8", errors="replace")

        result = {
            "success": True,
            "secret_id": normalized.get("name", secret_name),
            "arn": normalized.get("arn", ""),
            "version_id": normalized.get("version_id", ""),
            "version_stage": version_stage,
            "api_key": secret_value,
        }
        return result

    except Exception as e:
        if hasattr(e, "response") and "Error" in e.response:
            error_info = handle_secrets_error(e)
            return {
                "success": False,
                "secret_id": secret_name,
                "version_stage": version_stage,
                "error_code": error_info.get("error_code", ""),
                "error_message": error_info.get("error_message", str(e)),
                "request_id": error_info.get("request_id", ""),
            }
        return {
            "success": False,
            "secret_id": secret_name,
            "version_stage": version_stage,
            "error_code": "CLIENT_ERROR",
            "error_message": str(e),
        }
