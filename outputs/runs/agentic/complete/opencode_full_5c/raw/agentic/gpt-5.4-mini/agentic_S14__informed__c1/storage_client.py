import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass
class StorageConfig:
    bucket: str
    region: Optional[str] = None
    endpoint_url: Optional[str] = None


def load_storage_config(bucket: Optional[str] = None) -> StorageConfig:
    resolved_bucket = (
        bucket or os.environ.get("STORAGE_BUCKET") or os.environ.get("S3_BUCKET") or ""
    )
    if not resolved_bucket:
        raise ValueError("bucket is required")
    return StorageConfig(
        bucket=resolved_bucket,
        region=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
    )


def s3_client():
    kwargs = {}
    endpoint_url = os.environ.get("S3_ENDPOINT_URL")
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
    if region:
        kwargs["region_name"] = region
    return boto3.client("s3", **kwargs)
