import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass
class StorageConfig:
    bucket: Optional[str] = None
    region: Optional[str] = None
    endpoint_url: Optional[str] = None


def load_storage_config() -> StorageConfig:
    return StorageConfig(
        bucket=os.getenv("S3_BUCKET"),
        region=os.getenv("AWS_REGION"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    )


def get_s3_client():
    config = load_storage_config()
    kwargs = {}
    if config.region:
        kwargs["region_name"] = config.region
    if config.endpoint_url:
        kwargs["endpoint_url"] = config.endpoint_url
    return boto3.client("s3", **kwargs)


def resolve_bucket(bucket: Optional[str] = None) -> str:
    value = bucket or load_storage_config().bucket
    if not value:
        raise ValueError("bucket is required")
    return value
