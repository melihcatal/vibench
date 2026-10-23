import os
from typing import Dict, Optional

import boto3


def aws_region() -> str:
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"


def kms_client():
    return boto3.client("kms", region_name=aws_region())


def kms_key_id(default: Optional[str] = None) -> str:
    return os.environ.get("AWS_KMS_KEY_ID") or os.environ.get("KMS_KEY_ID") or (default or "")


def encryption_context() -> Dict[str, str]:
    context = {}
    for key in ("APP_NAME", "ENVIRONMENT", "DATA_CLASSIFICATION"):
        value = os.environ.get(key)
        if value:
            context[key.lower()] = value
    return context
