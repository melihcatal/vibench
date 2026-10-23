from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


DEFAULT_AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_S3_BUCKET = os.getenv("S3_BUCKET")
DEFAULT_S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")


def get_aws_region(explicit_region: Optional[str] = None) -> str:
    return explicit_region or DEFAULT_AWS_REGION


def get_default_bucket(explicit_bucket: Optional[str] = None) -> str:
    bucket = explicit_bucket or DEFAULT_S3_BUCKET
    if not bucket:
        raise ValueError("S3 bucket is required. Set S3_BUCKET or pass bucket explicitly.")
    return bucket


def build_boto_config() -> Config:
    return Config(
        region_name=get_aws_region(),
        retries={"max_attempts": 10, "mode": "standard"},
        signature_version="s3v4",
    )


def get_s3_client(region: Optional[str] = None, endpoint_url: Optional[str] = None) -> BaseClient:
    return boto3.client(
        "s3",
        region_name=get_aws_region(region),
        endpoint_url=endpoint_url or DEFAULT_S3_ENDPOINT_URL,
        config=build_boto_config(),
    )


def get_textract_client(region: Optional[str] = None) -> BaseClient:
    return boto3.client(
        "textract",
        region_name=get_aws_region(region),
        config=build_boto_config(),
    )


def get_translate_client(region: Optional[str] = None) -> BaseClient:
    return boto3.client(
        "translate",
        region_name=get_aws_region(region),
        config=build_boto_config(),
    )
