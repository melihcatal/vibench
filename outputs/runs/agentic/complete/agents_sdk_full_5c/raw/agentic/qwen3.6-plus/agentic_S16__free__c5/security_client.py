"""
security_client.py - Provide local configuration and client helper utilities for Secret Management.

Provides configuration loading, AWS Secrets Manager client initialization,
retry logic, and common response parsing utilities used across integration files.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import (
    SecretMetadata,
    SecretResponse,
    SecretVersionInfo,
    SecretRotationStatus,
    normalize_datetime,
    normalize_secret_value,
    parse_json_secret_value,
)

logger = logging.getLogger(__name__)

# Provider-specific AWS Secrets Manager endpoint configuration
AWS_SECRETS_MANAGER_ENDPOINT = os.environ.get(
    "AWS_SECRETS_MANAGER_ENDPOINT",
    "https://secretsmanager.us-east-1.amazonaws.com",
)
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_SECRET_ARN_PREFIX = os.environ.get("AWS_SECRET_ARN_PREFIX", "arn:aws:secretsmanager")


def load_aws_config() -> Dict[str, Any]:
    """
    Load AWS configuration from environment variables with sensible defaults.

    Returns a configuration dictionary suitable for boto3 client initialization.
    """
    config = {
        "region_name": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "aws_session_token": os.environ.get("AWS_SESSION_TOKEN", ""),
        "endpoint_url": os.environ.get(
            "AWS_SECRETS_MANAGER_ENDPOINT",
            "https://secretsmanager.us-east-1.amazonaws.com",
        ),
    }
    # Remove empty credentials for use with IAM roles or localstack
    if not config["aws_access_key_id"]:
        del config["aws_access_key_id"]
    if not config["aws_secret_access_key"]:
        del config["aws_secret_access_key"]
    if not config["aws_session_token"]:
        del config["aws_session_token"]
    return config


def get_secrets_manager_client() -> boto3.client:
    """
    Create and return a configured boto3 Secrets Manager client.

    Uses AWS SDK (boto3) with retry configuration for resilience.
    Provider: AWS Secrets Manager (secretsmanager.amazonaws.com)
    """
    aws_config = load_aws_config()
    boto_config = Config(
        retries={"max_attempts": 5, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )

    client_kwargs = {"config": boto_config}
    region = aws_config.pop("region_name", "us-east-1")

    if "aws_access_key_id" in aws_config:
        client_kwargs["aws_access_key_id"] = aws_config["aws_access_key_id"]
    if "aws_secret_access_key" in aws_config:
        client_kwargs["aws_secret_access_key"] = aws_config["aws_secret_access_key"]
    if "aws_session_token" in aws_config:
        client_kwargs["aws_session_token"] = aws_config["aws_session_token"]

    client = boto3.client("secretsmanager", region_name=region, **client_kwargs)
    return client


def resolve_secret_id(secret_identifier: str) -> str:
    """
    Resolve a secret identifier to a full ARN if needed.

    Supports short names, partial ARNs, and full ARNs.
    """
    if secret_identifier.startswith("arn:aws:secretsmanager"):
        return secret_identifier
    return secret_identifier


def handle_aws_client_error(error: ClientError, secret_id: str) -> SecretResponse:
    """
    Convert an AWS ClientError into a normalized SecretResponse.

    Handles common AWS Secrets Manager error codes.
    """
    error_code = error.response["Error"]["Code"]
    error_message = error.response["Error"]["Message"]

    return SecretResponse(
        success=False,
        secret_id=secret_id,
        error_message=f"AWS Secrets Manager error [{error_code}]: {error_message}",
        raw_response={"Error": error.response["Error"]},
    )


def parse_describe_secret_response(
    describe_response: Dict[str, Any],
) -> SecretMetadata:
    """
    Parse a boto3 describe_secret response into a SecretMetadata object.
    """
    version_ids = []
    for version_id, version_stages in describe_response.get("VersionIdsToStages", {}).items():
        version_ids.append(version_id)

    rotation_rules = describe_response.get("RotationRules", {})
    rotation_interval = rotation_rules.get("AutomaticallyAfterDays", 0)

    last_rotated = normalize_datetime(describe_response.get("LastRotatedDate"))
    next_rotation = normalize_datetime(describe_response.get("NextRotationDate"))
    created_date = normalize_datetime(describe_response.get("CreatedDate"))

    status_map = {
        True: SecretRotationStatus.ACTIVE,
    }
    is_deleted = describe_response.get("DeletedDate") is not None
    status = SecretRotationStatus.PENDING_DELETION if is_deleted else SecretRotationStatus.ACTIVE

    metadata = SecretMetadata(
        secret_id=describe_response.get("ARN", ""),
        name=describe_response.get("Name", ""),
        description=describe_response.get("Description", ""),
        labels=describe_response.get("VersionIdsToStages", {}).keys(),
        rotation_enabled=describe_response.get("RotationEnabled", False),
        rotation_lambda_arn=describe_response.get("RotationLambdaARN"),
        rotation_interval_days=rotation_interval,
        last_rotated_date=last_rotated,
        next_rotation_date=next_rotation,
        created_date=created_date,
        status=status,
        version_ids=version_ids,
        tags={tag["Key"]: tag["Value"] for tag in describe_response.get("Tags", [])},
    )
    return metadata


def parse_get_secret_value_response(
    get_response: Dict[str, Any], secret_id: str
) -> SecretResponse:
    """
    Parse a boto3 get_secret_value response into a normalized SecretResponse.
    """
    version_info = SecretVersionInfo(
        version_id=get_response.get("VersionId", ""),
        stage=get_response.get("VersionStage", "AWSCURRENT"),
        created_date=normalize_datetime(get_response.get("CreatedDate")),
        is_current=get_response.get("VersionStage", "") == "AWSCURRENT",
        secret_string=get_response.get("SecretString"),
        secret_binary=get_response.get("SecretBinary"),
    )

    secret_value = normalize_secret_value(
        get_response.get("SecretString") or get_response.get("SecretBinary")
    )

    return SecretResponse(
        success=True,
        secret_id=secret_id,
        secret_value=secret_value,
        secret_value_bytes=get_response.get("SecretBinary"),
        version_id=get_response.get("VersionId"),
        stage=get_response.get("VersionStage", "AWSCURRENT"),
        version_info=version_info,
        raw_response=get_response,
    )


def get_secret_stages(client: boto3.client, secret_id: str) -> Dict[str, List[str]]:
    """
    Retrieve version-to-stages mapping for a secret from AWS Secrets Manager.
    """
    try:
        describe_resp = client.describe_secret(SecretId=secret_id)
        return describe_resp.get("VersionIdsToStages", {})
    except ClientError as e:
        logger.error("Failed to describe secret %s: %s", secret_id, e)
        return {}


def list_secrets_by_tag(
    client: boto3.client, tag_key: str, tag_value: str
) -> List[Dict[str, Any]]:
    """
    List secrets filtered by a specific tag using AWS Secrets Manager filter API.
    """
    filters = [{"Key": "tag-key", "Values": [tag_key]}, {"Key": "tag-value", "Values": [tag_value]}]
    secrets = []
    paginator = client.get_paginator("list_secrets")
    for page in paginator.paginate(Filters=filters):
        secrets.extend(page.get("SecretList", []))
    return secrets
