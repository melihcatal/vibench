from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"
S3_BUCKET_ENV = "S3_BUCKET"
S3_ENDPOINT_URL_ENV = "S3_ENDPOINT_URL"
S3_SIGNATURE_VERSION_ENV = "S3_SIGNATURE_VERSION"


@dataclass(frozen=True)
class StorageConfig:
    bucket: str
    region: str = "us-east-1"
    endpoint_url: Optional[str] = None
    signature_version: str = "s3v4"


def load_storage_config(bucket: Optional[str] = None) -> StorageConfig:
    resolved_bucket = bucket or os.getenv(S3_BUCKET_ENV)
    if not resolved_bucket:
        raise ValueError(f"Missing required bucket; set {S3_BUCKET_ENV} or pass bucket.")
    region = os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV) or "us-east-1"
    endpoint_url = os.getenv(S3_ENDPOINT_URL_ENV)
    signature_version = os.getenv(S3_SIGNATURE_VERSION_ENV, "s3v4")
    return StorageConfig(
        bucket=resolved_bucket,
        region=region,
        endpoint_url=endpoint_url,
        signature_version=signature_version,
    )


@lru_cache(maxsize=8)
def get_s3_client(region: Optional[str] = None, endpoint_url: Optional[str] = None, signature_version: str = "s3v4"):
    resolved_region = region or os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV) or "us-east-1"
    resolved_endpoint = endpoint_url or os.getenv(S3_ENDPOINT_URL_ENV)
    return boto3.client(
        "s3",
        region_name=resolved_region,
        endpoint_url=resolved_endpoint,
        config=Config(signature_version=signature_version),
    )


def handle_boto_error(exc: Exception) -> RuntimeError:
    if isinstance(exc, (ClientError, BotoCoreError)):
        return RuntimeError(str(exc))
    return RuntimeError(f"Unhandled storage error: {exc}")
