"""
Read a specific secret version or staged value from AWS Secrets Manager.

This module handles version-specific secret retrieval, allowing access
to historical versions and staged values (AWSPENDING, AWSCURRENT, etc.).
"""

import json
import logging
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from security_client import get_secrets_manager_client
from security_models import SecretFetchResult, SecretVersionInfo

logger = logging.getLogger(__name__)

AWS_PROVIDER_ID = "aws-secrets-manager"


def get_secret_version_id(
    secret_name: str,
    region_name: str = "us-east-1",
) -> Optional[str]:
    """
    Get the current version ID of a secret from AWS Secrets Manager.

    Args:
        secret_name: The secret name or ARN.
        region_name: AWS region.

    Returns:
        The version ID string or None.
    """
    result = rotate_secret_version(
        secret_name,
        version_id="AWSCURRENT",
        region_name=region_name,
    )
    if result.success:
        return result.version_id
    return None


def rotate_secret_version(
    secret_name: str,
    version_id: str = "AWSCURRENT",
    region_name: str = "us-east-1",
) -> SecretFetchResult:
    """
    Read a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_name: The secret name or ARN.
        version_id: The version ID or staging label (e.g., AWSCURRENT, AWSPENDING).
        region_name: AWS region.

    Returns:
        SecretFetchResult with the secret value for the requested version.
    """
    try:
        client = get_secrets_manager_client(region_name=region_name)

        is_stage_label = version_id in ("AWSCURRENT", "AWSPENDING", "AWSPREVIOUS")

        if is_stage_label:
            response = client.get_secret_value(
                SecretId=secret_name,
                VersionStage=version_id,
            )
        else:
            response = client.get_secret_value(
                SecretId=secret_name,
                VersionId=version_id,
            )

        secret_string = response.get("SecretString")
        parsed_data = None
        if secret_string:
            try:
                parsed_data = json.loads(secret_string)
            except json.JSONDecodeError:
                pass

        return SecretFetchResult(
            success=True,
            secret_name=secret_name,
            secret_value=secret_string,
            secret_data=parsed_data,
            version_id=response.get("VersionId"),
            version_stage=version_id if is_stage_label else None,
            arn=response.get("ARN"),
            provider=AWS_PROVIDER_ID,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        logger.error(
            "Error fetching version %s of secret %s from AWS: %s",
            version_id,
            secret_name,
            error_code,
        )
        return SecretFetchResult(
            success=False,
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            error=f"AWS error: {error_code}",
        )
    except Exception as e:
        return SecretFetchResult(
            success=False,
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            error=str(e),
        )


def list_secret_versions(
    secret_name: str, region_name: str = "us-east-1"
) -> List[SecretVersionInfo]:
    """
    List all versions of a secret in AWS Secrets Manager.

    Args:
        secret_name: The secret name or ARN.
        region_name: AWS region.

    Returns:
        List of SecretVersionInfo objects for each version.
    """
    try:
        client = get_secrets_manager_client(region_name=region_name)

        response = client.describe_secret(SecretId=secret_name)
        version_ids = response.get("VersionIdsToStages", {})

        versions = []
        for version_id, stages in version_ids.items():
            versions.append(
                SecretVersionInfo(
                    version_id=version_id,
                    stages=stages,
                    secret_name=secret_name,
                    provider=AWS_PROVIDER_ID,
                )
            )

        return versions

    except ClientError as e:
        logger.error(
            "Error listing versions for %s from AWS: %s",
            secret_name,
            e.response["Error"]["Code"],
        )
        return []
