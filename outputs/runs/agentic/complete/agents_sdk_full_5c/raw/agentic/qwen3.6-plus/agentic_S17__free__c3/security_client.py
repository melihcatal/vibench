"""
Local configuration and client helper utilities for Key Management and Encryption.

Provides AWS KMS client initialization, credential handling, and common
utilities for cryptographic operations using the boto3 SDK.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from functools import lru_cache

import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)

# AWS KMS provider signals
KMS_ENDPOINT_URL = "kms.amazonaws.com"
DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def get_aws_credentials() -> Dict[str, str]:
    """Retrieve AWS credentials from environment variables."""
    credentials = {}
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    session_token = os.environ.get("AWS_SESSION_TOKEN")

    if access_key:
        credentials["aws_access_key_id"] = access_key
    if secret_key:
        credentials["aws_secret_access_key"] = secret_key
    if session_token:
        credentials["aws_session_token"] = session_token

    return credentials


@lru_cache(maxsize=1)
def get_kms_client(region: Optional[str] = None, config_override: Optional[Dict[str, Any]] = None):
    """
    Initialize and return a cached AWS KMS boto3 client.

    Args:
        region: AWS region override (defaults to AWS_DEFAULT_REGION env var).
        config_override: Optional botocore config dict override.

    Returns:
        boto3 KMS client instance.
    """
    resolved_region = region or DEFAULT_REGION
    credentials = get_aws_credentials()

    botocore_config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        connect_timeout=5,
        read_timeout=30,
    )

    if config_override:
        botocore_config = Config(**config_override)

    return boto3.client(
        "kms",
        region_name=resolved_region,
        config=botocore_config,
        **credentials,
    )


def get_sts_client(region: Optional[str] = None):
    """Initialize an AWS STS boto3 client for identity/caller info."""
    resolved_region = region or DEFAULT_REGION
    credentials = get_aws_credentials()
    return boto3.client(
        "sts",
        region_name=resolved_region,
        **credentials,
    )


def get_cloudtrail_client(region: Optional[str] = None):
    """Initialize an AWS CloudTrail boto3 client for key usage auditing."""
    resolved_region = region or DEFAULT_REGION
    credentials = get_aws_credentials()
    return boto3.client(
        "cloudtrail",
        region_name=resolved_region,
        **credentials,
    )


def get_sagemaker_runtime_client(region: Optional[str] = None):
    """Initialize an AWS SageMaker Runtime client for embedding generation."""
    resolved_region = region or DEFAULT_REGION
    credentials = get_aws_credentials()
    return boto3.client(
        "sagemaker-runtime",
        region_name=resolved_region,
        **credentials,
    )


def get_translate_client(region: Optional[str] = None):
    """Initialize an AWS Translate boto3 client for translation services."""
    resolved_region = region or DEFAULT_REGION
    credentials = get_aws_credentials()
    return boto3.client(
        "translate",
        region_name=resolved_region,
        **credentials,
    )


def load_key_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load key management configuration from a JSON file or environment.

    Args:
        config_path: Path to JSON config file.

    Returns:
        Dictionary with key configuration values.
    """
    config = {
        "default_key_id": os.environ.get("AWS_KMS_DEFAULT_KEY_ID", ""),
        "signing_key_id": os.environ.get("AWS_KMS_SIGNING_KEY_ID", ""),
        "envelope_key_id": os.environ.get("AWS_KMS_ENVELOPE_KEY_ID", ""),
        "encryption_context": {},
        "region": os.environ.get("AWS_DEFAULT_REGION", DEFAULT_REGION),
    }

    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            file_config = json.load(f)
            config.update(file_config)

    return config


def validate_key_id(key_id: str) -> bool:
    """Validate that a key ID matches AWS KMS identifier patterns."""
    if not key_id:
        return False
    # UUID pattern
    if len(key_id) == 36 and key_id.count("-") == 4:
        return True
    # ARN pattern
    if key_id.startswith("arn:aws:kms:"):
        return True
    # Multi-region key pattern
    if key_id.startswith("mrk-"):
        return True
    # Alias pattern
    if key_id.startswith("alias/"):
        return True
    return False


def describe_key_metadata(key_id: str, client=None) -> Dict[str, Any]:
    """
    Retrieve metadata for an AWS KMS key.

    Args:
        key_id: The KMS key identifier.
        client: Optional pre-initialized KMS client.

    Returns:
        Dictionary with key metadata.
    """
    if client is None:
        client = get_kms_client()
    response = client.describe_key(KeyId=key_id)
    return response.get("KeyMetadata", {})


def build_encryption_context(tags: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Build an AWS KMS encryption context dictionary."""
    context = {
        "purpose": "data-protection",
        "environment": os.environ.get("ENVIRONMENT", "production"),
    }
    if tags:
        context.update({str(k): str(v) for k, v in tags.items()})
    return context
