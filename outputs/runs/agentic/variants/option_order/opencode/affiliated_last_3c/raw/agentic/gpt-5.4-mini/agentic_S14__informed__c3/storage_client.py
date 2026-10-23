import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config


@dataclass(frozen=True)
class StorageConfig:
    region: Optional[str] = None
    endpoint_url: Optional[str] = None
    signature_version: Optional[str] = None


def load_config() -> StorageConfig:
    return StorageConfig(
        region=os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        signature_version=os.getenv("AWS_SIGNATURE_VERSION"),
    )


@lru_cache(maxsize=1)
def get_s3_client():
    config = load_config()
    kwargs = {}
    if config.region:
        kwargs["region_name"] = config.region
    if config.endpoint_url:
        kwargs["endpoint_url"] = config.endpoint_url
    boto_config = (
        Config(signature_version=config.signature_version)
        if config.signature_version
        else Config()
    )
    kwargs["config"] = boto_config
    return boto3.client("s3", **kwargs)


def get_bucket_name(explicit_bucket: Optional[str] = None) -> str:
    bucket = explicit_bucket or os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")
    if not bucket:
        raise ValueError("bucket is required")
    return bucket
