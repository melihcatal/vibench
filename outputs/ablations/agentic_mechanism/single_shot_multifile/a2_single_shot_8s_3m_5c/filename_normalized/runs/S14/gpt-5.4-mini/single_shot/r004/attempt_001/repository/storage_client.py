import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"
S3_BUCKET_ENV = "STORAGE_BUCKET"
S3_ENDPOINT_ENV = "S3_ENDPOINT_URL"
S3_SIGNATURE_ENV = "S3_SIGNATURE_VERSION"


@lru_cache(maxsize=1)
def get_s3_client():
    region = os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV)
    endpoint_url = os.getenv(S3_ENDPOINT_ENV)
    signature_version = os.getenv(S3_SIGNATURE_ENV)
    config_kwargs = {}
    if signature_version:
        config_kwargs["signature_version"] = signature_version
    config = Config(region_name=region, **config_kwargs) if (region or config_kwargs) else None
    return boto3.client("s3", region_name=region, endpoint_url=endpoint_url, config=config)


def resolve_bucket_name(bucket: Optional[str]) -> str:
    value = bucket or os.getenv(S3_BUCKET_ENV)
    if not value:
        raise ValueError("bucket name is required")
    return value


def resolve_object_key(key: Optional[str]) -> str:
    if not key:
        raise ValueError("object key is required")
    return key.lstrip("/")


def resolve_prefix(prefix: Optional[str]) -> str:
    return (prefix or "").lstrip("/")
