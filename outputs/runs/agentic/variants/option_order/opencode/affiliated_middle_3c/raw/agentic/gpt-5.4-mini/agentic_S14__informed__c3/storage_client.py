import os
from dataclasses import dataclass
from functools import lru_cache

import boto3


@dataclass(frozen=True)
class StorageConfig:
    bucket: str
    region: str | None
    endpoint_url: str | None


def load_storage_config() -> StorageConfig:
    bucket = os.environ.get("STORAGE_BUCKET", os.environ.get("AWS_S3_BUCKET", ""))
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    endpoint_url = os.environ.get("S3_ENDPOINT_URL")
    return StorageConfig(bucket=bucket, region=region, endpoint_url=endpoint_url)


@lru_cache(maxsize=1)
def get_s3_client():
    config = load_storage_config()
    kwargs = {}
    if config.region:
        kwargs["region_name"] = config.region
    if config.endpoint_url:
        kwargs["endpoint_url"] = config.endpoint_url
    return boto3.client("s3", **kwargs)


def resolve_bucket(bucket: str | None = None) -> str:
    resolved = bucket or load_storage_config().bucket
    if not resolved:
        raise ValueError("bucket is required")
    return resolved
