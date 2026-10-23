"""Provide local configuration and client helper utilities for Key Management and Encryption."""

import base64
import os
from typing import Optional, Dict

import boto3
from botocore.config import Config


def load_aws_credentials() -> Dict[str, str]:
    """Load AWS credentials from environment variables."""
    access_key = os.environ.get("AWS_ACCESS_KEY_ID", "")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    if not access_key or not secret_key:
        raise EnvironmentError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set for AWS KMS integration."
        )
    return {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
    }


def get_kms_client(region: str = "us-east-1") -> boto3.client:
    """Create and return a configured AWS KMS client."""
    creds = load_aws_credentials()
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=5,
        read_timeout=30,
    )
    kms = boto3.client(
        "kms",
        region_name=region,
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        config=config,
    )
    return kms


def base64_encode_bytes(data: bytes) -> str:
    """Encode bytes to base64 string."""
    return base64.b64encode(data).decode("utf-8")


def base64_decode_string(data: str) -> bytes:
    """Decode a base64 string to bytes."""
    return base64.b64decode(data)


def build_encryption_context(**kwargs: str) -> Dict[str, str]:
    """Build an AWS KMS encryption context dict from keyword arguments."""
    return {k: v for k, v in kwargs.items() if v}


def ensure_binary(plaintext: bytes | str) -> bytes:
    """Ensure plaintext is bytes."""
    if isinstance(plaintext, str):
        return plaintext.encode("utf-8")
    return plaintext


def ensure_text(data: bytes | str) -> str:
    """Ensure data is text."""
    if isinstance(data, bytes):
        return data.decode("utf-8")
    return data


def get_default_key_id() -> str:
    """Get default KMS key ID from environment or raise."""
    key_id = os.environ.get("AWS_KMS_KEY_ID", "")
    if not key_id:
        raise EnvironmentError(
            "AWS_KMS_KEY_ID environment variable must be set."
        )
    return key_id
