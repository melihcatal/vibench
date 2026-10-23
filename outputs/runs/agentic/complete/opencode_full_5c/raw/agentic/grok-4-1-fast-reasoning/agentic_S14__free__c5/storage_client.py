import os
import boto3
from botocore.config import Config
from typing import Optional


def create_aws_client(service: str, region: Optional[str] = None):
    region = region or os.getenv("AWS_REGION", "us-east-1")
    return boto3.client(
        service,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region,
        config=Config(connect_timeout=10, read_timeout=10, retries={"max_attempts": 3}),
    )
