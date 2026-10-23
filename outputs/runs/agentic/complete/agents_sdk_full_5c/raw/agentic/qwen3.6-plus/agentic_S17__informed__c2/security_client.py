"""
security_client.py - Provide local configuration and client helper utilities
for Key Management and Encryption using AWS KMS.
"""

import os
import base64
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config


def get_kms_client(
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> Any:
    """
    Create and return a boto3 KMS client using AWS KMS provider credentials.
    Uses environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    and AWS_DEFAULT_REGION when explicit parameters are not provided.
    """
    region = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    access_key = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", "")
    secret_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", "")

    session_kwargs: Dict[str, Any] = {"region_name": region}
    if access_key and secret_key:
        session_kwargs["aws_access_key_id"] = access_key
        session_kwargs["aws_secret_access_key"] = secret_key

    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        read_timeout=30,
        connect_timeout=10,
    )

    client_kwargs: Dict[str, Any] = {"config": config}
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url

    kms_client = boto3.client("kms", **session_kwargs, **client_kwargs)
    return kms_client


def build_encryption_context(
    context_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    additional: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    context: Dict[str, str] = {}
    if context_type:
        context["context_type"] = context_type
    if resource_id:
        context["resource_id"] = resource_id
    if additional:
        context.update(additional)
    return context


def resolve_key_id(key_id_or_alias: str) -> str:
    """
    Resolve a KMS key alias to its ARN when an alias is provided.
    Aliases should be prefixed with 'alias/'.
    """
    if key_id_or_alias.startswith("alias/"):
        return key_id_or_alias
    return key_id_or_alias


def validate_ciphertext_blob(ciphertext_b64: str) -> bytes:
    """Decode and validate a base64-encoded ciphertext blob."""
    ciphertext = base64.b64decode(ciphertext_b64)
    if not ciphertext or len(ciphertext) < 16:
        raise ValueError("Ciphertext blob is too short or empty.")
    return ciphertext


def load_crypto_config() -> Dict[str, Any]:
    """Load encryption configuration from environment variables."""
    return {
        "kms_key_id": os.environ.get("KMS_KEY_ID", ""),
        "signing_key_id": os.environ.get("KMS_SIGNING_KEY_ID", ""),
        "region": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        "encryption_algorithm": os.environ.get("KMS_ENCRYPTION_ALGORITHM", "SYMMETRIC_DEFAULT"),
        "signing_algorithm": os.environ.get("KMS_SIGNING_ALGORITHM", "ECDSA_SHA_256"),
    }
