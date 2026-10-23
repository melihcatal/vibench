from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_s3_client(service_name: str = "s3") -> BaseClient:
    endpoint_url: Optional[str] = os.getenv("AWS_S3_ENDPOINT_URL")
    return boto3.client(
        service_name,
        region_name=get_aws_region(),
        endpoint_url=endpoint_url,
        config=Config(signature_version="s3v4"),
    )


def get_textract_client() -> BaseClient:
    return boto3.client("textract", region_name=get_aws_region())


def get_translate_client() -> BaseClient:
    return boto3.client("translate", region_name=get_aws_region())


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key
