import os
from functools import lru_cache

import boto3
from botocore.config import Config


def _env(name, default=None):
    value = os.getenv(name)
    return value if value not in (None, "") else default


def storage_settings():
    return {
        "region_name": _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1")),
        "signature_version": _env("AWS_S3_SIGNATURE_VERSION", "s3v4"),
        "endpoint_url": _env("AWS_S3_ENDPOINT_URL"),
        "bucket": _env("AWS_S3_BUCKET", _env("S3_BUCKET")),
    }


@lru_cache(maxsize=1)
def s3_client():
    settings = storage_settings()
    return boto3.client(
        "s3",
        region_name=settings["region_name"],
        endpoint_url=settings["endpoint_url"],
        config=Config(signature_version=settings["signature_version"]),
    )


def default_bucket(explicit_bucket=None):
    bucket = explicit_bucket or storage_settings()["bucket"]
    if not bucket:
        raise ValueError("bucket is required")
    return bucket
