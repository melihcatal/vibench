import os
from functools import lru_cache

import boto3


@lru_cache(maxsize=1)
def get_s3_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.client("s3", region_name=region)


def get_default_bucket() -> str:
    bucket = os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")
    if not bucket:
        raise ValueError("Missing S3_BUCKET or AWS_S3_BUCKET")
    return bucket
