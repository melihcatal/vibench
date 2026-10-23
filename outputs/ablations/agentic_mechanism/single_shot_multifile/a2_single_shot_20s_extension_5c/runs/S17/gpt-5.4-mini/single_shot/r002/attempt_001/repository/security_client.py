from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient

AWS_DEFAULT_REGION_ENV = "AWS_REGION"
AWS_KMS_KEY_ID_ENV = "AWS_KMS_KEY_ID"


def resolve_region() -> str:
    return os.environ.get(AWS_DEFAULT_REGION_ENV) or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"


def resolve_kms_key_id(explicit_key_id: Optional[str] = None) -> str:
    value = explicit_key_id or os.environ.get(AWS_KMS_KEY_ID_ENV)
    if not value:
        raise ValueError("AWS KMS key id is required")
    return value


@lru_cache(maxsize=8)
def build_kms_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("kms", region_name=region_name or resolve_region())
