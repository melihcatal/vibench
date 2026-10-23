import os
import boto3
from typing import Optional


def get_s3_client(region: Optional[str] = None) -> boto3.client:
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region or os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
