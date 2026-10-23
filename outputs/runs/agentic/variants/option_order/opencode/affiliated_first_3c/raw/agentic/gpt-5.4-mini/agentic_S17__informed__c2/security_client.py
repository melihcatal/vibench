import os
from typing import Any, Dict

import boto3

from security_models import normalize_metadata, normalize_text


def load_security_config() -> Dict[str, str]:
    return {
        "aws_region": os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
        "kms_key_id": normalize_text(os.getenv("AWS_KMS_KEY_ID", "")),
    }


def kms_client():
    cfg = load_security_config()
    return boto3.client("kms", region_name=cfg["aws_region"])


def normalize_key_id(value: Any) -> str:
    return normalize_text(value)


def normalize_payload(value: Any) -> str:
    return normalize_text(value)


def normalize_event(event: Dict[str, Any]) -> Dict[str, str]:
    return normalize_metadata(event)
