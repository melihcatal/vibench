"""
security_client.py - Provide local configuration and client helper utilities
for Key Management and Encryption using AWS KMS.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


class SecurityClientConfig:
    """Configuration container for AWS KMS client setup."""

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        region_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        max_retries: int = 3,
        kms_endpoint: Optional[str] = None,
    ):
        self.aws_access_key_id = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_session_token = aws_session_token or os.environ.get("AWS_SESSION_TOKEN")
        self.region_name = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.endpoint_url = endpoint_url or kms_endpoint
        self.max_retries = max_retries

    @classmethod
    def from_env(cls, prefix: str = "KMS") -> "SecurityClientConfig":
        """Load configuration from environment variables with optional prefix."""
        return cls(
            aws_access_key_id=os.environ.get(f"{prefix}_AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get(f"{prefix}_AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get(f"{prefix}_AWS_REGION"),
            kms_endpoint=os.environ.get(f"{prefix}_ENDPOINT_URL"),
            max_retries=int(os.environ.get(f"{prefix}_MAX_RETRIES", "3")),
        )

    @classmethod
    def from_file(cls, config_path: str) -> "SecurityClientConfig":
        """Load configuration from a JSON config file."""
        with open(config_path, "r") as f:
            data = json.load(f)
        return cls(
            aws_access_key_id=data.get("aws_access_key_id"),
            aws_secret_access_key=data.get("aws_secret_access_key"),
            aws_session_token=data.get("aws_session_token"),
            region_name=data.get("region_name"),
            endpoint_url=data.get("endpoint_url"),
            max_retries=data.get("max_retries", 3),
        )


def create_kms_client(config: Optional[SecurityClientConfig] = None) -> Any:
    """
    Create a configured boto3 AWS KMS client.
    Uses AWS KMS service endpoint: kms.{region}.amazonaws.com
    """
    if config is None:
        config = SecurityClientConfig()

    client_kwargs: Dict[str, Any] = {
        "service_name": "kms",
        "region_name": config.region_name,
        "config": Config(
            retries={"max_attempts": config.max_retries, "mode": "standard"}
        ),
    }

    if config.aws_access_key_id:
        client_kwargs["aws_access_key_id"] = config.aws_access_key_id
    if config.aws_secret_access_key:
        client_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
    if config.aws_session_token:
        client_kwargs["aws_session_token"] = config.aws_session_token
    if config.endpoint_url:
        client_kwargs["endpoint_url"] = config.endpoint_url

    return boto3.client(**client_kwargs)


def create_kms_data_key_client(config: Optional[SecurityClientConfig] = None) -> Any:
    """Create a boto3 AWS KMS client for data key operations."""
    return create_kms_client(config)


def handle_kms_error(error: ClientError, context: str = "") -> None:
    """Handle and log AWS KMS errors consistently."""
    error_code = error.response["Error"]["Code"]
    error_message = error.response["Error"]["Message"]
    prefix = f"[KMS Error in {context}] " if context else "[KMS Error] "
    raise RuntimeError(f"{prefix}{error_code}: {error_message}") from error


def extract_key_arn_from_response(response: Dict[str, Any], default_key: str = "") -> str:
    """Extract the key ARN or ID from a KMS API response."""
    return response.get("KeyId", default_key)


def get_default_key_id() -> str:
    """Retrieve the default KMS key ID from environment."""
    return os.environ.get("KMS_DEFAULT_KEY_ID", "")
