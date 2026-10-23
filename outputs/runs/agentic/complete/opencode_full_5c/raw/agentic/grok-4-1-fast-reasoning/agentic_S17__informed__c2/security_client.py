import boto3
from typing import Optional


def get_kms_client(region: Optional[str] = None) -> boto3.client:
    if region is None:
        region = "us-east-1"
    return boto3.client("kms", region_name=region)
