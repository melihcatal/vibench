from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config


@dataclass(frozen=True)
class StorageConfig:
    aws_region: str
    bucket_name: str
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    endpoint_url: Optional[str] = None


@lru_cache(maxsize=1)
def load_storage_config() -> StorageConfig:
    return StorageConfig(
        aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        bucket_name=os.environ["S3_BUCKET_NAME"],
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    )


@lru_cache(maxsize=1)
def get_s3_client():
    cfg = load_storage_config()
    return boto3.client(
        "s3",
        region_name=cfg.aws_region,
        endpoint_url=cfg.endpoint_url,
        aws_access_key_id=cfg.aws_access_key_id,
        aws_secret_access_key=cfg.aws_secret_access_key,
        aws_session_token=cfg.aws_session_token,
        config=Config(signature_version="s3v4"),
    )


def get_bucket_name() -> str:
    return load_storage_config().bucket_name
