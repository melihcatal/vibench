from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from boto3.session import Session
from botocore.client import Config

DEFAULT_S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
DEFAULT_S3_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_S3_BUCKET = os.getenv("S3_BUCKET")


@dataclass(frozen=True)
class StorageConfig:
    bucket: str
    region_name: str = DEFAULT_S3_REGION
    endpoint_url: Optional[str] = DEFAULT_S3_ENDPOINT_URL
    signature_version: str = "s3v4"


def load_storage_config(bucket: Optional[str] = None) -> StorageConfig:
    resolved_bucket = bucket or DEFAULT_S3_BUCKET
    if not resolved_bucket:
        raise ValueError("S3 bucket is required via argument or S3_BUCKET environment variable")
    return StorageConfig(bucket=resolved_bucket)


@lru_cache(maxsize=1)
def get_session() -> Session:
    return boto3.session.Session()


def get_s3_client(config: Optional[StorageConfig] = None):
    cfg = config or load_storage_config()
    return get_session().client(
        "s3",
        region_name=cfg.region_name,
        endpoint_url=cfg.endpoint_url,
        config=Config(signature_version=cfg.signature_version),
    )
