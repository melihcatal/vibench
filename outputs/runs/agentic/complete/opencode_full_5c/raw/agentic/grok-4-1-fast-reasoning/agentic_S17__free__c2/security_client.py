import boto3
import os
from typing import Any


def get_kms_client() -> Any:
    return boto3.client("kms", region_name=os.getenv("AWS_REGION", "us-east-1"))
