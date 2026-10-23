from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import boto3
from boto3.client import BaseClient
from botocore.config import Config


AWS_REGION_ENV = "AWS_REGION"
AWS_PROFILE_ENV = "AWS_PROFILE"
AWS_ENDPOINT_URL_ENV = "AWS_ENDPOINT_URL"
AWS_S3_ADDRESSING_STYLE_ENV = "AWS_S3_ADDRESSING_STYLE"


@lru_cache(maxsize=1)
def get_s3_client(
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    signature_version: str = "s3v4",
) -> BaseClient:
    session = boto3.session.Session(profile_name=os.getenv(AWS_PROFILE_ENV) or None)
    config = Config(
        signature_version=signature_version,
        s3={"addressing_style": os.getenv(AWS_S3_ADDRESSING_STYLE_ENV, "auto")},
    )
    return session.client(
        "s3",
        region_name=region_name or os.getenv(AWS_REGION_ENV) or None,
        endpoint_url=endpoint_url or os.getenv(AWS_ENDPOINT_URL_ENV) or None,
        config=config,
    )


def resolve_bucket_name(bucket: Optional[str]) -> str:
    if bucket:
        return bucket
    env_bucket = os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")
    if not env_bucket:
        raise ValueError("bucket is required")
    return env_bucket


def resolve_key(key: Optional[str]) -> str:
    if key:
        return key
    env_key = os.getenv("S3_KEY") or os.getenv("AWS_S3_KEY")
    if not env_key:
        raise ValueError("key is required")
    return env_key
