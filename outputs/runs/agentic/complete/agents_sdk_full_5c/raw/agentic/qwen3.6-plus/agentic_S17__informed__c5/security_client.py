"""
Local configuration and client helper utilities for Key Management and Encryption.
Provides connection setup, credential handling, and shared KMS client utilities
for AWS Key Management Service integrations.
"""

import os
import base64
from typing import Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


# ---------------------------------------------------------------------------
# Environment / Configuration Helpers
# ---------------------------------------------------------------------------

def get_aws_kms_config() -> dict:
    """Return AWS KMS configuration loaded from environment variables."""
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_session_token": os.getenv("AWS_SESSION_TOKEN"),
        "region_name": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    }


def get_kms_key_id() -> Optional[str]:
    """Return the configured AWS KMS key identifier."""
    return os.getenv("AWS_KMS_KEY_ID")


# ---------------------------------------------------------------------------
# KMS Client Construction
# ---------------------------------------------------------------------------

def build_kms_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    region_name: Optional[str] = None,
) -> boto3.client:
    """Create and return a configured boto3 KMS client."""
    config = Config(
        retries={"max_attempts": 5, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )

    kwargs: dict = {
        "service_name": "kms",
        "region_name": region_name or get_aws_kms_config()["region_name"],
        "config": config,
    }

    if aws_access_key_id:
        kwargs["aws_access_key_id"] = aws_access_key_id
    if aws_secret_access_key:
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token:
        kwargs["aws_session_token"] = aws_session_token

    return boto3.client(**kwargs)


def get_default_kms_client() -> boto3.client:
    """Build a KMS client using environment-based credentials."""
    cfg = get_aws_kms_config()
    return build_kms_client(
        aws_access_key_id=cfg["aws_access_key_id"],
        aws_secret_access_key=cfg["aws_secret_access_key"],
        aws_session_token=cfg["aws_session_token"],
        region_name=cfg["region_name"],
    )


# ---------------------------------------------------------------------------
# Encoding / Decoding Helpers
# ---------------------------------------------------------------------------

def base64_encode_bytes(data: bytes) -> str:
    """Encode raw bytes to a base64 string."""
    return base64.b64encode(data).decode("utf-8")


def base64_decode_string(data: str) -> bytes:
    """Decode a base64 string back to raw bytes."""
    return base64.b64decode(data)


# ---------------------------------------------------------------------------
# Error Handling
# ---------------------------------------------------------------------------

class KMSError(Exception):
    """Base exception for KMS-related operations."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error


def handle_kms_error(exc: ClientError, context: str) -> KMSError:
    """Wrap a botocore ClientError into a KMSError with contextual info."""
    code = exc.response["Error"].get("Code", "Unknown")
    msg = exc.response["Error"].get("Message", "")
    return KMSError(
        f"KMS error during {context}: [{code}] {msg}",
        original_error=exc,
    )
