"""
Local configuration and client helper utilities for Key Management and Encryption.
Provides AWS KMS client setup, credential handling, and shared utilities.
"""

import os
import logging
from typing import Optional, Dict, Any

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# AWS KMS defaults
DEFAULT_AWS_KMS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
DEFAULT_AWS_KMS_KEY_ID = os.environ.get("AWS_KMS_KEY_ID", "")


class SecurityClientConfig:
    """Configuration holder for security service clients."""

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        region_name: Optional[str] = None,
        kms_key_id: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        self.aws_access_key_id = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", "")
        self.aws_secret_access_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", "")
        self.aws_session_token = aws_session_token or os.environ.get("AWS_SESSION_TOKEN", "")
        self.region_name = region_name or DEFAULT_AWS_KMS_REGION
        self.kms_key_id = kms_key_id or DEFAULT_AWS_KMS_KEY_ID
        self.max_retries = max_retries
        self.timeout = timeout

    def has_credentials(self) -> bool:
        return bool(self.aws_access_key_id and self.aws_secret_access_key)


def create_kms_client(config: Optional[SecurityClientConfig] = None):
    """
    Create and return a configured boto3 KMS client for AWS Key Management Service.
    Uses aws_kms_hostname internally: kms.us-east-1.amazonaws.com
    """
    if config is None:
        config = SecurityClientConfig()

    client_kwargs = {
        "service_name": "kms",
        "region_name": config.region_name,
        "config": Config(
            retries={"max_attempts": config.max_retries},
            read_timeout=config.timeout,
            connect_timeout=config.timeout,
        ),
    }

    if config.has_credentials():
        client_kwargs["aws_access_key_id"] = config.aws_access_key_id
        client_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
        if config.aws_session_token:
            client_kwargs["aws_session_token"] = config.aws_session_token

    kms_client = boto3.client(**client_kwargs)
    logger.info("Created AWS KMS client for region %s", config.region_name)
    return kms_client


def get_default_key_id(config: Optional[SecurityClientConfig] = None) -> str:
    """Get the default KMS key ID from config or environment."""
    if config is None:
        config = SecurityClientConfig()
    if not config.kms_key_id:
        raise ValueError("KMS_KEY_ID is not set. Provide it via environment or config.")
    return config.kms_key_id


def handle_kms_error(error: ClientError, operation: str) -> Dict[str, Any]:
    """Handle and log AWS KMS errors with structured output."""
    error_code = error.response["Error"]["Code"]
    error_message = error.response["Error"]["Message"]
    request_id = error.response.get("ResponseMetadata", {}).get("RequestId", "")

    logger.error(
        "AWS KMS %s error [%s]: %s (request_id=%s)",
        operation,
        error_code,
        error_message,
        request_id,
    )
    return {
        "error_code": error_code,
        "error_message": error_message,
        "request_id": request_id,
        "operation": operation,
    }


def validate_key_id(key_id: str) -> bool:
    """Validate that a KMS key ID looks like a valid AWS KMS key identifier."""
    if not key_id:
        return False
    valid_prefixes = ("arn:aws:kms:", "mrk-", "alias/")
    return (
        any(key_id.startswith(p) for p in valid_prefixes)
        or len(key_id) == 36
    )


def build_encryption_context(*args, **kwargs) -> Dict[str, str]:
    """Build a normalized encryption context dict for KMS operations."""
    context = {}
    for item in args:
        if isinstance(item, dict):
            context.update({str(k): str(v) for k, v in item.items()})
    context.update({str(k): str(v) for k, v in kwargs.items()})
    return context


def describe_key(kms_client, key_id: str) -> Dict[str, Any]:
    """Describe a KMS key and return its metadata."""
    try:
        response = kms_client.describe_key(KeyId=key_id)
        return response.get("KeyMetadata", {})
    except ClientError as e:
        return handle_kms_error(e, "describe_key")
