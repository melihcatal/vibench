"""
security_client.py - Local configuration and client helper utilities for Secret Management.

Provides functions to configure and create boto3 clients for AWS Secrets Manager,
load configuration from environment, and wrap common operations with error handling.
"""

from __future__ import annotations

import os
import logging
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

AWS_SECRETS_MANAGER_ENDPOINT = "secretsmanager.amazonaws.com"
DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


def get_secretsmanager_client(
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> Any:
    """
    Create and return a configured boto3 Secrets Manager client.

    Args:
        region_name: AWS region (falls back to DEFAULT_REGION env var).
        endpoint_url: Optional custom endpoint (for LocalStack or testing).

    Returns:
        boto3 Secrets Manager client instance.
    """
    region = region_name or DEFAULT_REGION
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region,
    )
    kwargs: Dict[str, Any] = {"service_name": "secretsmanager", "region_name": region}
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
    client = session.client(**kwargs)
    logger.info("Created AWS Secrets Manager client (region=%s, endpoint=%s)", region, endpoint_url or AWS_SECRETS_MANAGER_ENDPOINT)
    return client


def get_secret_value(
    client: Any,
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieve a secret value with optional version or stage filtering.

    Args:
        client: boto3 Secrets Manager client.
        secret_id: Secret name or ARN.
        version_id: Specific version ID to retrieve.
        version_stage: Version stage (e.g., AWSCURRENT, AWSPENDING).

    Returns:
        Raw response dict from GetSecretValue.
    """
    kwargs: Dict[str, Any] = {"SecretId": secret_id}
    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage:
        kwargs["VersionStage"] = version_stage

    try:
        response = client.get_secret_value(**kwargs)
        return response
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        logger.error("Failed to get secret %s (error=%s): %s", secret_id, error_code, e)
        raise


def describe_secret(client: Any, secret_id: str) -> Dict[str, Any]:
    """
    Describe a secret to get metadata including rotation config and version list.

    Args:
        client: boto3 Secrets Manager client.
        secret_id: Secret name or ARN.

    Returns:
        Raw response dict from DescribeSecret.
    """
    try:
        return client.describe_secret(SecretId=secret_id)
    except ClientError as e:
        logger.error("Failed to describe secret %s: %s", secret_id, e)
        raise


def list_secret_versions(
    client: Any,
    secret_id: str,
    max_results: int = 100,
) -> Dict[str, Any]:
    """
    List all versions of a secret.

    Args:
        client: boto3 Secrets Manager client.
        secret_id: Secret name or ARN.
        max_results: Maximum number of versions to return.

    Returns:
        Raw response dict from ListSecretVersionIds.
    """
    return client.list_secret_version_ids(
        SecretId=secret_id,
        MaxResults=max_results,
        IncludeDeprecated=True,
    )


def load_rotation_config() -> Dict[str, Any]:
    """
    Load rotation configuration from environment variables.

    Returns:
        Dict with rotation_enabled, lambda_arn, and rotation_rules.
    """
    return {
        "rotation_enabled": os.getenv("SECRET_ROTATION_ENABLED", "false").lower() == "true",
        "lambda_arn": os.getenv("SECRET_ROTATION_LAMBDA_ARN", ""),
        "rotation_rules": {
            "automatically_after_days": int(os.getenv("SECRET_ROTATION_DAYS", "30")),
        },
    }


def build_secret_tags(
    environment: str = "production",
    team: str = "platform",
    compliance: str = "pci",
) -> list:
    """Build a list of tag dicts for secret creation or updates."""
    return [
        {"Key": "Environment", "Value": environment},
        {"Key": "Team", "Value": team},
        {"Key": "Compliance", "Value": compliance},
    ]
