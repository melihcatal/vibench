import os
from typing import Optional

import boto3
from botocore.config import Config


def get_region(default: str = "us-east-1") -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or default


def get_bucket_env_name() -> str:
    return os.getenv("STORAGE_BUCKET_ENV", "STORAGE_BUCKET")


def resolve_bucket(bucket: Optional[str] = None) -> str:
    if bucket:
        return bucket
    env_bucket = os.getenv(get_bucket_env_name())
    if env_bucket:
        return env_bucket
    raise ValueError("bucket is required")


def create_s3_client(region: Optional[str] = None):
    return boto3.client(
        "s3",
        region_name=region or get_region(),
        config=Config(signature_version="s3v4"),
    )


def get_ocr_provider_region() -> str:
    return get_region()


def get_textract_client(region: Optional[str] = None):
    return boto3.client("textract", region_name=region or get_region())


def get_translate_client(region: Optional[str] = None):
    return boto3.client("translate", region_name=region or get_region())


def get_bedrock_client(region: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region or get_region())
