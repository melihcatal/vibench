"""
security_client.py - Local configuration and client helper utilities for Key Management and Encryption.

Provides AWS KMS client initialization, credential loading, retry configuration,
and utility functions for interacting with the AWS Key Management Service.
"""

import os
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
DEFAULT_RETRY_ATTEMPTS = int(os.environ.get("AWS_RETRY_ATTEMPTS", "3"))


def get_kms_client(
    region_name: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> boto3.client:
    """
    Initialize and return an AWS KMS client using boto3.

    Uses environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN, and AWS_DEFAULT_REGION if explicit parameters are not provided.
    """
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    access_key = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY")
    session_token = aws_session_token or os.environ.get("AWS_SESSION_TOKEN")

    retry_config = Config(
        retries={"max_attempts": DEFAULT_RETRY_ATTEMPTS, "mode": "adaptive"},
        region_name=region,
    )

    session_kwargs: Dict[str, Any] = {
        "config": retry_config,
    }

    if endpoint_url:
        session_kwargs["endpoint_url"] = endpoint_url
    if access_key:
        session_kwargs["aws_access_key_id"] = access_key
    if secret_key:
        session_kwargs["aws_secret_access_key"] = secret_key
    if session_token:
        session_kwargs["aws_session_token"] = session_token

    kms_client = boto3.client("kms", **session_kwargs)
    return kms_client


def get_kms_key_metadata(kms_client: boto3.client, key_id: str) -> Dict[str, Any]:
    """
    Retrieve metadata for a KMS key using the DescribeKey API.

    Returns key state, key usage, creation date, and origin information.
    """
    try:
        response = kms_client.describe_key(KeyId=key_id)
        return response["KeyMetadata"]
    except ClientError as e:
        raise RuntimeError(f"Failed to describe KMS key {key_id}: {e}") from e


def list_kms_keys(kms_client: boto3.client, limit: int = 100) -> list:
    """
    List KMS keys accessible in the account.
    Returns a list of key metadata dicts.
    """
    keys = []
    paginator = kms_client.get_paginator("list_keys")
    for page in paginator.paginate(PaginationConfig={"MaxItems": limit}):
        keys.extend(page.get("Keys", []))
    return keys


def load_encryption_context(context_str: Optional[str]) -> Dict[str, str]:
    """
    Parse a JSON string into an encryption context dict.
    Returns an empty dict if context_str is None or empty.
    """
    import json

    if not context_str:
        return {}
    try:
        ctx = json.loads(context_str)
        return {str(k): str(v) for k, v in ctx.items()}
    except (json.JSONDecodeError, TypeError):
        return {}


def validate_key_id(key_id: str) -> None:
    """
    Validate that a KMS key ID matches expected formats.
    Accepts key IDs, key ARNs, or alias names.
    """
    import re

    if not key_id:
        raise ValueError("Key ID cannot be empty")

    key_id_pattern = re.compile(
        r"^"
        r"(?:arn:aws:kms:[a-z0-9-]+:\d{12}:key/[a-f0-9-]+)"
        r"|(?:mrk-[a-f0-9]{32})"
        r"|(?:[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"
        r"|(?:alias/[a-zA-Z0-9/_-]+)"
        r"$"
    )
    if not key_id_pattern.match(key_id):
        raise ValueError(f"Invalid KMS key ID format: {key_id}")
