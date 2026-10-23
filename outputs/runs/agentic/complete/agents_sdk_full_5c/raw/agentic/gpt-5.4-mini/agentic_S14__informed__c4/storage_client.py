from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient

from storage_models import normalize_metadata

S3_ENDPOINT_ENV = "AWS_S3_ENDPOINT_URL"
S3_BUCKET_ENV = "AWS_S3_BUCKET"


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    return boto3.client(
        "s3",
        endpoint_url=os.getenv(S3_ENDPOINT_ENV),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def default_bucket() -> Optional[str]:
    return os.getenv(S3_BUCKET_ENV)


def coerce_bucket(bucket: Optional[str]) -> str:
    value = bucket or default_bucket()
    if not value:
        raise ValueError(f"Bucket must be provided or set via {S3_BUCKET_ENV}")
    return value


def put_object(bucket: str, key: str, body, content_type: Optional[str] = None, metadata=None):
    kwargs = {"Bucket": bucket, "Key": key, "Body": body}
    if content_type:
        kwargs["ContentType"] = content_type
    norm = normalize_metadata(metadata)
    if norm:
        kwargs["Metadata"] = norm
    return get_s3_client().put_object(**kwargs)
