from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient

AWS_DEFAULT_REGION_ENV = "AWS_REGION"
AWS_ALT_REGION_ENV = "AWS_DEFAULT_REGION"
S3_BUCKET_ENV = "S3_BUCKET_NAME"


@lru_cache(maxsize=1)
def get_s3_client(region_name: Optional[str] = None) -> BaseClient:
    region = region_name or os.getenv(AWS_DEFAULT_REGION_ENV) or os.getenv(AWS_ALT_REGION_ENV)
    if region:
        return boto3.client("s3", region_name=region)
    return boto3.client("s3")


@lru_cache(maxsize=1)
def get_s3_resource(region_name: Optional[str] = None):
    region = region_name or os.getenv(AWS_DEFAULT_REGION_ENV) or os.getenv(AWS_ALT_REGION_ENV)
    if region:
        return boto3.resource("s3", region_name=region)
    return boto3.resource("s3")


def resolve_bucket(default: Optional[str] = None) -> str:
    bucket = default or os.getenv(S3_BUCKET_ENV)
    if not bucket:
        raise ValueError("S3 bucket name is required via parameter or S3_BUCKET_NAME")
    return bucket
