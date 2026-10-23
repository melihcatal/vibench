"""
rotate_secret_version.py - Reads a specific secret version or staged value from AWS Secrets Manager.

Uses boto3 to interact with secretsmanager.amazonaws.com to retrieve
a particular version of a secret, including AWSPENDING and AWSCURRENT stages.
"""

from __future__ import annotations

import logging
from typing import Optional, Dict, Any

from security_client import (
    get_secretsmanager_client,
    get_secret_value,
    describe_secret,
    list_secret_versions,
)
from security_models import SecretResponse, SecretVersionInfo

logger = logging.getLogger(__name__)


def rotate_secret_version(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: str = "AWSPENDING",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Read a specific secret version or staged value for rotation purposes.

    During rotation, AWSPENDING holds the new value being rotated in.
    This function retrieves that staged value for validation or comparison.

    Args:
        secret_name: The name or ARN of the secret.
        version_id: Explicit version ID to read.
        version_stage: Stage to read (AWSPENDING for rotation, AWSCURRENT for current).
        region: AWS region override.

    Returns:
        Dict with version info, parsed value, and comparison metadata.
    """
    client = get_secretsmanager_client(region_name=region)
    logger.info(
        "Reading secret version from AWS Secrets Manager: %s (stage=%s, version=%s)",
        secret_name,
        version_stage,
        version_id or "auto",
    )

    secret_value_resp = get_secret_value(
        client,
        secret_id=secret_name,
        version_id=version_id,
        version_stage=version_stage,
    )

    metadata = describe_secret(client, secret_name)

    secret_response = SecretResponse.from_aws_response(secret_value_resp, metadata)

    result = {
        "secret_name": secret_response.name,
        "arn": secret_response.arn,
        "version_id": secret_response.version_id,
        "version_stages": secret_response.version_stages,
        "value": secret_response.value,
        "rotation_enabled": secret_response.rotation_enabled,
        "rotation_lambda_arn": secret_response.rotation_lambda_arn,
        "last_rotated_date": secret_response.last_rotated_date,
    }

    logger.info("Read version %s with stages %s", result["version_id"], result["version_stages"])
    return result


def get_all_versions(
    secret_name: str,
    region: Optional[str] = None,
) -> Dict[str, SecretVersionInfo]:
    """
    List all versions of a secret with their stage information.

    Args:
        secret_name: The name or ARN of the secret.
        region: AWS region override.

    Returns:
        Dict mapping version_id to SecretVersionInfo.
    """
    client = get_secretsmanager_client(region_name=region)
    resp = list_secret_versions(client, secret_name)

    versions = {}
    for v in resp.get("Versions", []):
        info = SecretVersionInfo.from_aws_response(v)
        versions[info.version_id] = info

    logger.info("Found %d versions for secret %s", len(versions), secret_name)
    return versions


def compare_versions(
    secret_name: str,
    current_stage: str = "AWSCURRENT",
    pending_stage: str = "AWSPENDING",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Compare the current and pending versions of a secret during rotation.

    Args:
        secret_name: The name or ARN of the secret.
        current_stage: Stage for current value.
        pending_stage: Stage for pending (new) value.
        region: AWS region override.

    Returns:
        Dict with both values and a boolean indicating if they differ.
    """
    current = rotate_secret_version(secret_name, version_stage=current_stage, region=region)
    pending = rotate_secret_version(secret_name, version_stage=pending_stage, region=region)

    return {
        "secret_name": secret_name,
        "current_version_id": current["version_id"],
        "pending_version_id": pending["version_id"],
        "values_match": current["value"] == pending["value"],
        "current_stages": current["version_stages"],
        "pending_stages": pending["version_stages"],
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    secret_name = "production/db/postgres-main"
    result = rotate_secret_version(secret_name, version_stage="AWSPENDING")
    print(f"Pending version: {result['version_id']}")
    print(f"Stages: {result['version_stages']}")
