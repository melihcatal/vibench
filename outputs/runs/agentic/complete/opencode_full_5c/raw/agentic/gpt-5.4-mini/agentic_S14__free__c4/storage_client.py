import os
from functools import lru_cache

import boto3


@lru_cache(maxsize=1)
def get_s3_client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client("s3", region_name=region)


def get_bucket_name(explicit=None):
    return explicit or os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")


def get_object_key(explicit=None):
    return explicit or os.getenv("S3_OBJECT_KEY")
