import boto3
import os
from typing import Optional


def get_kms_client(region: Optional[str] = None):
    region = region or os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("kms", region_name=region)


def get_kms_key_id():
    key_id = os.getenv("KMS_KEY_ID")
    if not key_id:
        raise ValueError("KMS_KEY_ID environment variable is required.")
    return key_id
