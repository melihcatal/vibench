from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config


@dataclass(frozen=True)
class StorageConfig:
    bucket_name: str
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None
    object_prefix: str = ""
    presign_expires_in: int = 3600


@lru_cache(maxsize=1)
def load_config() -> StorageConfig:
    return StorageConfig(
        bucket_name=os.environ.get("S3_BUCKET", os.environ.get("AWS_S3_BUCKET", "")),
        region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
        object_prefix=os.environ.get("S3_OBJECT_PREFIX", ""),
        presign_expires_in=int(os.environ.get("S3_PRESIGN_EXPIRES_IN", "3600")),
    )


@lru_cache(maxsize=1)
def s3_client():
    config = load_config()
    boto_config = Config(signature_version="s3v4")
    kwargs = {"config": boto_config}
    if config.region_name:
        kwargs["region_name"] = config.region_name
    if config.endpoint_url:
        kwargs["endpoint_url"] = config.endpoint_url
    return boto3.client("s3", **kwargs)


def resolve_key(key: str) -> str:
    config = load_config()
    prefix = config.object_prefix.strip("/")
    key = key.lstrip("/")
    if prefix:
        return f"{prefix}/{key}"
    return key
