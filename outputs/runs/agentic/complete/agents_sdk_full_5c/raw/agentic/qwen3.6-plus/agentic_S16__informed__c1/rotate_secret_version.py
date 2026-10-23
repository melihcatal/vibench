"""
Reads a specific secret version or staged value from AWS Secrets Manager.

Retrieves secrets by version ID or version stage (AWSCURRENT, AWSPENDING, etc.)
and supports comparing versions during rotation operations.

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
    SecretResponse,
    normalize_aws_response_to_secret_response,
    build_error_secret_response,
)


def get_secret_version(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve a specific version of a secret from AWS Secrets Manager.

    Can identify the version either by explicit VersionId or by VersionStage.
    If neither is specified, defaults to the AWSCURRENT stage.

    Args:
        secret_name: The name or ARN of the secret.
        version_id: Optional specific version UUID to retrieve.
        version_stage: Optional version stage label (e.g., AWSPENDING).
        region: Optional AWS region override.

    Returns:
        Dictionary with the secret value and version metadata.
    """
    try:
        client = create_secrets_manager_client(region=region)

        kwargs: Dict[str, Any] = {"SecretId": secret_name}
        if version_id:
            kwargs["VersionId"] = version_id
        if version_stage:
            kwargs["VersionStage"] = version_stage

        response = client.get_secret_value(**kwargs)

        secret_value = response.get("SecretString", "")
        if not secret_value and "SecretBinary" in response:
            secret_value = response["SecretBinary"].decode("utf-8", errors="replace")

        result = {
            "success": True,
            "secret_id": response.get("Name", secret_name),
            "arn": response.get("ARN", ""),
            "version_id": response.get("VersionId", ""),
            "version_stages": response.get("VersionStage", []),
            "secret_value": secret_value,
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


def get_secret_version_stages(
    secret_name: str,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List all version stages for a secret in AWS Secrets Manager.

    Returns a mapping of version IDs to their associated stage labels,
    which is useful during rotation to identify current vs pending values.

    Args:
        secret_name: The name or ARN of the secret.
        region: Optional AWS region override.

    Returns:
        Dictionary mapping version IDs to lists of stage labels.
    """
    try:
        client = create_secrets_manager_client(region=region)

        describe_response = client.describe_secret(SecretId=secret_name)

        version_ids_to_stages: Dict[str, List[str]] = {}
        versions = describe_response.get("VersionIdsToStages", {})
        for version_id, stages in versions.items():
            version_ids_to_stages[version_id] = stages

        result = {
            "success": True,
            "secret_id": describe_response.get("Name", secret_name),
            "arn": describe_response.get("ARN", ""),
            "version_stages": version_ids_to_stages,
            "rotation_enabled": describe_response.get("RotationEnabled", False),
            "rotation_lambda_arn": describe_response.get("RotationLambdaARN"),
            "last_changed_date": describe_response.get("LastChangedDate"),
            "last_rotated_date": describe_response.get("LastRotatedDate"),
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


def get_pending_secret_value(
    secret_name: str,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve the AWSPENDING version of a secret during rotation.

    Args:
        secret_name: The name or ARN of the secret.
        region: Optional AWS region override.

    Returns:
        Dictionary with the pending secret value and version details.
    """
    return get_secret_version(
        secret_name=secret_name,
        version_stage="AWSPENDING",
        region=region,
    )


def compare_secret_versions(
    secret_name: str,
    version_id_a: str,
    version_id_b: str,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Compare two versions of a secret from AWS Secrets Manager.

    Fetches both versions and reports whether the values are identical.
    For JSON secrets, performs a deep comparison of parsed values.

    Args:
        secret_name: The name or ARN of the secret.
        version_id_a: First version ID to compare.
        version_id_b: Second version ID to compare.
        region: Optional AWS region override.

    Returns:
        Dictionary with comparison results and both values.
    """
    result_a = get_secret_version(secret_name, version_id=version_id_a, region=region)
    result_b = get_secret_version(secret_name, version_id=version_id_b, region=region)

    if not result_a.get("success") or not result_b.get("success"):
        return {
            "success": False,
            "secret_id": secret_name,
            "error_code": "VERSION_FETCH_FAILED",
            "error_message": "One or both versions could not be retrieved.",
            "version_a_result": result_a,
            "version_b_result": result_b,
        }

    value_a = result_a.get("secret_value", "")
    value_b = result_b.get("secret_value", "")

    are_equal = value_a == value_b

    try:
        parsed_a = json.loads(value_a)
        parsed_b = json.loads(value_b)
        json_equal = parsed_a == parsed_b
        is_json = True
    except (json.JSONDecodeError, TypeError):
        json_equal = are_equal
        is_json = False

    return {
        "success": True,
        "secret_id": secret_name,
        "values_identical": are_equal,
        "json_values_identical": json_equal if is_json else None,
        "is_json_secret": is_json,
        "version_a": {
            "version_id": version_id_a,
            "stages": result_a.get("version_stages", []),
            "value_length": len(value_a),
        },
        "version_b": {
            "version_id": version_id_b,
            "stages": result_b.get("version_stages", []),
            "value_length": len(value_b),
        },
    }
