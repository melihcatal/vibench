import os
from typing import Any, Dict, Optional

import boto3


def load_security_config() -> Dict[str, Any]:
    return {
        "aws_region": os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        "kms_key_id": os.environ.get("AWS_KMS_KEY_ID", "alias/key-management-demo"),
        "signing_key_id": os.environ.get("AWS_KMS_SIGNING_KEY_ID", os.environ.get("AWS_KMS_KEY_ID", "alias/key-management-demo")),
    }


def create_kms_client(region_name: Optional[str] = None):
    config = load_security_config()
    return boto3.client("kms", region_name=region_name or config["aws_region"])


def get_kms_key_id() -> str:
    return load_security_config()["kms_key_id"]


def get_signing_key_id() -> str:
    return load_security_config()["signing_key_id"]


def bytes_to_b64(data: bytes) -> str:
    import base64
    return base64.b64encode(data).decode("utf-8")


def b64_to_bytes(text: str) -> bytes:
    import base64
    return base64.b64decode(text.encode("utf-8"))
