from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


DEFAULT_S3_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
DEFAULT_SIGNATURE_VERSION = os.getenv("AWS_S3_SIGNATURE_VERSION", "s3v4")


@lru_cache(maxsize=4)
def get_s3_client(
    service_name: str = "s3",
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> BaseClient:
    session = boto3.session.Session(region_name=region_name or DEFAULT_S3_REGION)
    return session.client(
        service_name,
        region_name=region_name or DEFAULT_S3_REGION,
        endpoint_url=endpoint_url or DEFAULT_S3_ENDPOINT_URL,
        config=Config(signature_version=DEFAULT_SIGNATURE_VERSION),
    )


def get_textract_client(region_name: Optional[str] = None) -> BaseClient:
    return get_s3_client(service_name="textract", region_name=region_name)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value
