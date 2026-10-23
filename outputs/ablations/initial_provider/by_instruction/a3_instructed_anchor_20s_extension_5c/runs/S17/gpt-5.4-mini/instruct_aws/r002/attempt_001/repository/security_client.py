from __future__ import annotations

import os
from typing import Any, Dict, Optional

import boto3


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_kms_key_id() -> str:
    return os.getenv("AWS_KMS_KEY_ID", "alias/example-key")


def kms_client(region_name: Optional[str] = None):
    return boto3.client("kms", region_name=region_name or get_aws_region())


def normalize_response(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}
