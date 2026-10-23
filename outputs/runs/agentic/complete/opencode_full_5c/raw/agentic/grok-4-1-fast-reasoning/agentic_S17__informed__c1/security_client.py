import os
from typing import Dict, Any


def get_kms_config() -> Dict[str, Any]:
    return {
        "region_name": os.getenv("AWS_REGION", "us-east-1"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }


def get_key_id() -> str:
    return os.getenv("KEY_ID", "alias/my-key")
