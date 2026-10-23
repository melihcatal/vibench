import base64
import os
from typing import Dict, Optional

import boto3

from security_models import normalize_context


def get_kms_client():
    return boto3.client("kms", region_name=os.getenv("AWS_REGION"))


def get_default_key_id() -> str:
    key_id = os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID is required")
    return key_id


def to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def from_b64(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def normalize_encryption_context(context: Optional[Dict[str, str]]) -> Dict[str, str]:
    return normalize_context(context)
