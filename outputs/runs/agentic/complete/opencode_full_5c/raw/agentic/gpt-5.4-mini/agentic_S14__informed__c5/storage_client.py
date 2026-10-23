import os
from functools import lru_cache

import boto3
from botocore.client import Config


def storage_settings():
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_session_token": os.getenv("AWS_SESSION_TOKEN"),
        "region_name": os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1",
        "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
        "signature_version": os.getenv("S3_SIGNATURE_VERSION", "s3v4"),
    }


@lru_cache(maxsize=1)
def get_s3_client():
    settings = storage_settings()
    return boto3.client(
        "s3",
        aws_access_key_id=settings["aws_access_key_id"],
        aws_secret_access_key=settings["aws_secret_access_key"],
        aws_session_token=settings["aws_session_token"],
        region_name=settings["region_name"],
        endpoint_url=settings["endpoint_url"],
        config=Config(signature_version=settings["signature_version"]),
    )


def get_bucket_name(bucket: str | None = None) -> str:
    return bucket or os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET") or ""
