"""
Local helper: security_client.py
Provide local configuration and client helper utilities for Key Management and Encryption.
Uses AWS KMS (boto3) as the concrete provider for managed key operations.
"""

import os
import base64
import json
from typing import Optional, Dict, Any

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# AWS KMS provider identification
AWS_KMS_ENDPOINT = "kms.amazonaws.com"
AWS_KMS_SERVICE_NAME = "kms"


class KMSClientConfig:
    """Configuration helper for AWS KMS client."""

    def __init__(
        self,
        region: Optional[str] = None,
        kms_key_id: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        max_retries: int = 3,
        connect_timeout: int = 5,
        read_timeout: int = 30,
    ):
        self.region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.kms_key_id = kms_key_id or os.environ.get("AWS_KMS_KEY_ID")
        self.aws_access_key_id = aws_access_key_id or os.environ.get(
            "AWS_ACCESS_KEY_ID"
        )
        self.aws_secret_access_key = aws_secret_access_key or os.environ.get(
            "AWS_SECRET_ACCESS_KEY"
        )
        self.aws_session_token = aws_session_token or os.environ.get(
            "AWS_SESSION_TOKEN"
        )
        self.max_retries = max_retries
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

    def to_dict(self) -> Dict[str, Any]:
        return {
            "region": self.region,
            "kms_key_id": self.kms_key_id,
            "max_retries": self.max_retries,
            "connect_timeout": self.connect_timeout,
            "read_timeout": self.read_timeout,
        }


def create_kms_client(config: Optional[KMSClientConfig] = None):
    """
    Create an AWS KMS client with the provided or default configuration.
    Provider: AWS KMS (kms.amazonaws.com)
    """
    if config is None:
        config = KMSClientConfig()

    botocore_config = Config(
        retries={"max_attempts": config.max_retries},
        connect_timeout=config.connect_timeout,
        read_timeout=config.read_timeout,
    )

    session_kwargs = {"region_name": config.region}
    if config.aws_access_key_id and config.aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = config.aws_access_key_id
        session_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
    if config.aws_session_token:
        session_kwargs["aws_session_token"] = config.aws_session_token

    session = boto3.Session(**session_kwargs)
    kms_client = session.client(
        service_name=AWS_KMS_SERVICE_NAME, config=botocore_config
    )
    return kms_client


def create_sts_client(config: Optional[KMSClientConfig] = None):
    """Create an AWS STS client for caller identity verification."""
    if config is None:
        config = KMSClientConfig()

    session_kwargs = {"region_name": config.region}
    if config.aws_access_key_id and config.aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = config.aws_access_key_id
        session_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
    if config.aws_session_token:
        session_kwargs["aws_session_token"] = config.aws_session_token

    session = boto3.Session(**session_kwargs)
    return session.client("sts", config=Config(retries={"max_attempts": 3}))


def encode_ciphertext_blob(ciphertext: bytes) -> str:
    """Base64-encode a KMS ciphertext blob for safe transport."""
    return base64.b64encode(ciphertext).decode("utf-8")


def decode_ciphertext_blob(encoded_ciphertext: str) -> bytes:
    """Base64-decode a KMS ciphertext blob."""
    return base64.b64decode(encoded_ciphertext.encode("utf-8"))


def handle_kms_error(error: ClientError, operation: str) -> Dict[str, Any]:
    """Format a KMS ClientError into a structured response dict."""
    error_code = error.response.get("Error", {}).get("Code", "Unknown")
    error_message = error.response.get("Error", {}).get("Message", str(error))
    return {
        "success": False,
        "operation": operation,
        "error_code": error_code,
        "error_message": error_message,
        "provider": AWS_KMS_SERVICE_NAME,
        "endpoint": AWS_KMS_ENDPOINT,
    }
