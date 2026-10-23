import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config

DEFAULT_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


@lru_cache(maxsize=1)
def get_s3_client():
    endpoint_url = os.getenv("AWS_S3_ENDPOINT_URL")
    return boto3.client(
        "s3",
        region_name=DEFAULT_REGION,
        endpoint_url=endpoint_url,
        config=Config(signature_version="s3v4", retries={"max_attempts": 3, "mode": "standard"}),
    )


def resolve_bucket_name(bucket: Optional[str]) -> str:
    resolved = bucket or os.getenv("AWS_S3_BUCKET") or os.getenv("S3_BUCKET")
    if not resolved:
        raise ValueError("bucket is required")
    return resolved


def resolve_object_key(key: Optional[str]) -> str:
    if not key:
        raise ValueError("key is required")
    return key.lstrip("/")
