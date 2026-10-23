from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config
from botocore.exceptions import ClientError

DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_BUCKET = os.getenv("S3_BUCKET", "")


def get_s3_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client(
        "s3",
        region_name=region_name or DEFAULT_REGION,
        config=Config(signature_version="s3v4", retries={"max_attempts": 5, "mode": "standard"}),
    )


def get_textract_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("textract", region_name=region_name or DEFAULT_REGION)


def get_translate_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("translate", region_name=region_name or DEFAULT_REGION)


def require_bucket(bucket: Optional[str] = None) -> str:
    resolved = bucket or DEFAULT_BUCKET
    if not resolved:
        raise ValueError("An S3 bucket is required via argument or S3_BUCKET environment variable.")
    return resolved


def is_not_found_error(exc: ClientError) -> bool:
    code = exc.response.get("Error", {}).get("Code")
    return code in {"404", "NoSuchKey", "NotFound"}
