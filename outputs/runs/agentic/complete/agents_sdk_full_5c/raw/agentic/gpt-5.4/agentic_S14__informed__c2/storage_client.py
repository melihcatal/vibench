from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import boto3
from botocore.client import BaseClient
from botocore.config import Config

DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_SIGNATURE_VERSION = os.getenv("AWS_S3_SIGNATURE_VERSION", "s3v4")


def get_s3_client(service_name: str = "s3") -> BaseClient:
    config = Config(signature_version=DEFAULT_SIGNATURE_VERSION)
    session = boto3.session.Session(region_name=DEFAULT_REGION)
    endpoint_url = os.getenv("AWS_S3_ENDPOINT_URL") if service_name == "s3" else None
    return session.client(service_name, endpoint_url=endpoint_url, config=config)


@lru_cache(maxsize=1)
def s3_client() -> BaseClient:
    return get_s3_client("s3")


@lru_cache(maxsize=1)
def textract_client() -> BaseClient:
    return get_s3_client("textract")


@lru_cache(maxsize=1)
def translate_client() -> BaseClient:
    return get_s3_client("translate")


def require_bucket(bucket: str | None = None) -> str:
    resolved = bucket or os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")
    if not resolved:
        raise ValueError("bucket is required; set S3_BUCKET or AWS_S3_BUCKET")
    return resolved


def object_url(bucket: str, key: str, region: str | None = None) -> str:
    resolved_region = region or DEFAULT_REGION
    return f"s3://{bucket}/{key}?region={resolved_region}"


def compact_kwargs(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}
