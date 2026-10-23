import os
from typing import Any, Dict

import boto3


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def get_kms_client():
    return boto3.client("kms")


def get_region() -> str:
    return get_env("AWS_REGION", get_env("AWS_DEFAULT_REGION", "us-east-1"))


def key_metadata(key_id: str) -> Dict[str, Any]:
    return {"key_id": key_id, "provider": "aws-kms", "region": get_region()}
