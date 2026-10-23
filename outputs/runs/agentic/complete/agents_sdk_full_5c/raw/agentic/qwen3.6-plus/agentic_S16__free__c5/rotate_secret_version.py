"""
rotate_secret_version.py - Reads a specific secret version or staged value.

Uses AWS Secrets Manager (boto3 SDK) to read a specific version of a secret
by version ID or staging label, and also supports initiating rotation via
the rotate_secret API call.

Provider: AWS Secrets Manager (secretsmanager.us-east-1.amazonaws.com)
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from botocore.exceptions import ClientError

from security_client import (
    get_secrets_manager_client,
    resolve_secret_id,
    handle_aws_client_error,
    parse_get_secret_value_response,
    parse_describe_secret_response,
    get_secret_stages,
)
from security_models import (
    SecretResponse,
    SecretVersionInfo,
    SecretMetadata,
    SecretRotationStatus,
    normalize_datetime,
    normalize_secret_value,
)

logger = logging.getLogger(__name__)


def get_secret_version_by_id(
    secret_id: str,
    version_id: str,
) -> SecretResponse:
    """
    Retrieve a specific version of a secret by its VersionId from AWS Secrets Manager.

    Args:
        secret_id: The secret name or ARN.
        version_id: The specific VersionId string (e.g., from VersionIdsToStages).

    Returns:
        SecretResponse containing the specified version's value.
    """
    resolved_id = resolve_secret_id(secret_id)
    client = get_secrets_manager_client()

    try:
        response = client.get_secret_value(
            SecretId=resolved_id,
            VersionId=version_id,
        )
        return parse_get_secret_value_response(response, resolved_id)
    except ClientError as e:
        return handle_aws_client_error(e, resolved_id)
    except Exception as exc:
        logger.exception("Unexpected error fetching version %s of secret %s", version_id, resolved_id)
        return SecretResponse(
            success=False,
            secret_id=resolved_id,
            error_message=f"Unexpected error: {exc}",
        )


def get_secret_version_by_stage(
    secret_id: str,
    stage: str = "AWSCURRENT",
) -> SecretResponse:
    """
    Retrieve a secret version by its staging label from AWS Secrets Manager.

    Common staging labels:
    - AWSCURRENT: The current active version
    - AWSPENDING: The new version during rotation (before it becomes current)
    - AWSPREVIOUS: The previous version after rotation completes

    Args:
        secret_id: The secret name or ARN.
        stage: The staging label (AWSCURRENT, AWSPENDING, AWSPREVIOUS).

    Returns:
        SecretResponse containing the staged version's value.
    """
    resolved_id = resolve_secret_id(secret_id)
    client = get_secrets_manager_client()

    try:
        response = client.get_secret_value(
            SecretId=resolved_id,
            VersionStage=stage,
        )
        return parse_get_secret_value_response(response, resolved_id)
    except ClientError as e:
        return handle_aws_client_error(e, resolved_id)
    except Exception as exc:
        logger.exception("Unexpected error fetching stage %s of secret %s", stage, resolved_id)
        return SecretResponse(
            success=False,
            secret_id=resolved_id,
            error_message=f"Unexpected error: {exc}",
        )


def list_secret_versions(
    secret_id: str,
) -> Tuple[Optional[SecretMetadata], List[SecretVersionInfo]]:
    """
    List all versions and their stages for a secret in AWS Secrets Manager.

    Returns:
        Tuple of (metadata, list of version info objects).
    """
    resolved_id = resolve_secret_id(secret_id)
    client = get_secrets_manager_client()

    try:
        describe_resp = client.describe_secret(SecretId=resolved_id)
        metadata = parse_describe_secret_response(describe_resp)

        versions = []
        for version_id, stages in describe_resp.get("VersionIdsToStages", {}).items():
            version_info = SecretVersionInfo(
                version_id=version_id,
                stage=stages[0] if stages else "UNKNOWN",
                is_current="AWSCURRENT" in stages,
            )
            versions.append(version_info)

        return metadata, versions
    except ClientError as e:
        logger.error("Failed to list versions for secret %s: %s", resolved_id, e)
        return None, []


def initiate_secret_rotation(
    secret_id: str,
    rotation_lambda_arn: Optional[str] = None,
    rotation_rules: Optional[Dict[str, Any]] = None,
) -> SecretResponse:
    """
    Initiate secret rotation via AWS Secrets Manager rotate_secret API.

    Args:
        secret_id: The secret name or ARN.
        rotation_lambda_arn: Optional ARN of the Lambda function for rotation.
        rotation_rules: Optional dict with rotation schedule, e.g., {"AutomaticallyAfterDays": 30}.

    Returns:
        SecretResponse with the new VersionId of the rotated secret.
    """
    resolved_id = resolve_secret_id(secret_id)
    client = get_secrets_manager_client()

    try:
        kwargs: Dict[str, Any] = {"SecretId": resolved_id}
        if rotation_lambda_arn:
            kwargs["RotationLambdaARN"] = rotation_lambda_arn
        if rotation_rules:
            kwargs["RotationRules"] = rotation_rules

        rotation_response = client.rotate_secret(**kwargs)

        return SecretResponse(
            success=True,
            secret_id=resolved_id,
            version_id=rotation_response.get("VersionId"),
            raw_response=rotation_response,
        )
    except ClientError as e:
        return handle_aws_client_error(e, resolved_id)
    except Exception as exc:
        logger.exception("Unexpected error rotating secret %s", resolved_id)
        return SecretResponse(
            success=False,
            secret_id=resolved_id,
            error_message=f"Unexpected error: {exc}",
        )


def read_staged_secret_value(
    secret_id: str,
    stage: str = "AWSPENDING",
) -> SecretResponse:
    """
    Read a staged secret value (commonly used during rotation to verify the new value).

    Args:
        secret_id: The secret name or ARN.
        stage: The staging label (default AWSPENDING for in-progress rotations).

    Returns:
        SecretResponse containing the staged secret value.
    """
    return get_secret_version_by_stage(secret_id, stage)


def get_version_comparison(
    secret_id: str,
    version_a: str = "AWSCURRENT",
    version_b: str = "AWSPREVIOUS",
) -> Dict[str, Any]:
    """
    Compare two secret versions to detect changes.

    Args:
        secret_id: The secret name or ARN.
        version_a: First staging label or version ID.
        version_b: Second staging label or version ID.

    Returns:
        Dictionary with comparison details.
    """
    resp_a = get_secret_version_by_stage(secret_id, version_a) if not version_a.startswith("v-") else get_secret_version_by_id(secret_id, version_a)
    resp_b = get_secret_version_by_stage(secret_id, version_b) if not version_b.startswith("v-") else get_secret_version_by_id(secret_id, version_b)

    if not (resp_a.success and resp_b.success):
        return {
            "success": False,
            "error": f"Version A: {resp_a.error_message}, Version B: {resp_b.error_message}",
        }

    return {
        "success": True,
        "version_a_id": resp_a.version_id,
        "version_b_id": resp_b.version_id,
        "value_changed": resp_a.secret_value != resp_b.secret_value,
        "version_a_length": len(resp_a.secret_value) if resp_a.secret_value else 0,
        "version_b_length": len(resp_b.secret_value) if resp_b.secret_value else 0,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    secret_name = "prod/api/payment-key"
    metadata, versions = list_secret_versions(secret_name)
    if metadata:
        print(f"Secret: {metadata.name}, Versions: {len(versions)}")
        for v in versions:
            print(f"  Version: {v.version_id}, Stage: {v.stage}, Current: {v.is_current}")
    else:
        print("Failed to list versions")
