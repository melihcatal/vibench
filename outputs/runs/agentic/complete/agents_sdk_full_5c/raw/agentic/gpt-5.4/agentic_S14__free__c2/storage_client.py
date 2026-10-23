from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


AWS_REGION_ENV = "AWS_REGION"
S3_ENDPOINT_ENV = "S3_ENDPOINT_URL"
S3_ADDRESSING_STYLE_ENV = "S3_ADDRESSING_STYLE"
DEFAULT_REGION = "us-east-1"


@lru_cache(maxsize=1)
def get_aws_region() -> str:
    return os.getenv(AWS_REGION_ENV, DEFAULT_REGION)


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    endpoint_url: Optional[str] = os.getenv(S3_ENDPOINT_ENV)
    addressing_style = os.getenv(S3_ADDRESSING_STYLE_ENV, "auto")
    return session.client(
        "s3",
        endpoint_url=endpoint_url,
        config=Config(s3={"addressing_style": addressing_style}),
    )


@lru_cache(maxsize=1)
def get_textract_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client("textract")


@lru_cache(maxsize=1)
def get_translate_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client("translate")
