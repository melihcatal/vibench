import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config


@dataclass(frozen=True)
class StorageConfig:
    region_name: str
    endpoint_url: Optional[str]
    default_presign_expires_seconds: int


@lru_cache(maxsize=1)
def get_storage_config() -> StorageConfig:
    return StorageConfig(
        region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        default_presign_expires_seconds=int(os.getenv("DEFAULT_PRESIGN_EXPIRES_SECONDS", "900")),
    )


@lru_cache(maxsize=1)
def get_s3_client(config: Optional[StorageConfig] = None):
    cfg = config or get_storage_config()
    return boto3.client(
        "s3",
        region_name=cfg.region_name,
        endpoint_url=cfg.endpoint_url,
        config=Config(signature_version="s3v4"),
    )
