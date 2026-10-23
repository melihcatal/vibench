from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_s3_endpoint_url() -> Optional[str]:
    return os.getenv("AWS_S3_ENDPOINT_URL")


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client(
        "s3",
        endpoint_url=get_s3_endpoint_url(),
        config=Config(signature_version="s3v4"),
    )


@lru_cache(maxsize=1)
def get_textract_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client("textract")


@lru_cache(maxsize=1)
def get_translate_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_aws_region())
    return session.client("translate")
