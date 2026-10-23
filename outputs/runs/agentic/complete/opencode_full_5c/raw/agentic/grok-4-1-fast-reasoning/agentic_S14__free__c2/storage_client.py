import os
import boto3
from typing import Optional


def get_s3_client(region: Optional[str] = None) -> boto3.client:
    region = region or os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("s3", region_name=region)
