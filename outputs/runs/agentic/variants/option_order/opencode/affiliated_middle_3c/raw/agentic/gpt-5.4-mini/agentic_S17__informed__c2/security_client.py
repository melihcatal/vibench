import base64
import os
from functools import lru_cache
from typing import Dict, Optional

import boto3


def _kms_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.client("kms", region_name=region)


@lru_cache(maxsize=1)
def get_kms_client():
    return _kms_client()


def require_key_id() -> str:
    key_id = os.getenv("AWS_KMS_KEY_ID") or os.getenv("KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID is required")
    return key_id


def encryption_context(context: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    return dict(context or {})


def b64encode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def b64decode_text(value: str) -> bytes:
    return base64.b64decode(value.encode("ascii"))
