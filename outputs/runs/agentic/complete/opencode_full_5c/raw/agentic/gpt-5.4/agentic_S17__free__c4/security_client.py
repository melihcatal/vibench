from __future__ import annotations

import os
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def aws_region() -> str:
    return get_env("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def provider_name() -> str:
    return "aws_kms"


def kms_client() -> Any:
    return boto3.client(
        "kms",
        region_name=aws_region(),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def cloudtrail_client() -> Any:
    return boto3.client(
        "cloudtrail",
        region_name=aws_region(),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def normalize_encryption_context(context: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not context:
        return {}
    return {str(key): str(value) for key, value in context.items()}


def resolve_key_id(key_id: Optional[str]) -> str:
    return key_id or get_env("AWS_KMS_KEY_ID")
