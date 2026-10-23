from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.config import Config


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_default_bucket() -> Optional[str]:
    return os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")


def build_s3_client():
    return boto3.client(
        "s3",
        region_name=get_aws_region(),
        config=Config(signature_version="s3v4"),
    )


def build_s3_resource():
    return boto3.resource("s3", region_name=get_aws_region())


def build_s3_uri(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key}"


def require_bucket(bucket: Optional[str] = None) -> str:
    resolved = bucket or get_default_bucket()
    if not resolved:
        raise ValueError(
            "An S3 bucket is required via argument or S3_BUCKET/AWS_S3_BUCKET"
        )
    return resolved


def get_textract_client():
    return boto3.client("textract", region_name=get_aws_region())


def get_translate_client():
    return boto3.client("translate", region_name=get_aws_region())


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key
