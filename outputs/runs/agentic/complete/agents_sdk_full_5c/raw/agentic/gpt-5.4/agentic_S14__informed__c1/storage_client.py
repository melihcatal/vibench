from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


_DEFAULT_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
_DEFAULT_S3_ENDPOINT = os.getenv("S3_ENDPOINT_URL")
_DEFAULT_ADDRESSING_STYLE = os.getenv("S3_ADDRESSING_STYLE", "auto")


def get_aws_region(explicit_region: Optional[str] = None) -> str:
    return explicit_region or _DEFAULT_REGION


def get_s3_client(region_name: Optional[str] = None, endpoint_url: Optional[str] = None) -> BaseClient:
    return boto3.client(
        "s3",
        region_name=get_aws_region(region_name),
        endpoint_url=endpoint_url or _DEFAULT_S3_ENDPOINT,
        config=Config(s3={"addressing_style": _DEFAULT_ADDRESSING_STYLE}),
    )


def get_textract_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("textract", region_name=get_aws_region(region_name))


def get_translate_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("translate", region_name=get_aws_region(region_name))
