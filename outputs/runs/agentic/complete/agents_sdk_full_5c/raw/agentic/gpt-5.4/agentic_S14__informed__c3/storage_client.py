from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


DEFAULT_S3_SIGNATURE_VERSION = "s3v4"
DEFAULT_AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def get_s3_client(region_name: Optional[str] = None) -> BaseClient:
    session = boto3.session.Session(region_name=region_name or DEFAULT_AWS_REGION)
    return session.client(
        "s3",
        region_name=region_name or DEFAULT_AWS_REGION,
        config=Config(signature_version=DEFAULT_S3_SIGNATURE_VERSION),
    )


def get_textract_client(region_name: Optional[str] = None) -> BaseClient:
    session = boto3.session.Session(region_name=region_name or DEFAULT_AWS_REGION)
    return session.client("textract", region_name=region_name or DEFAULT_AWS_REGION)


def get_bucket_name(explicit_bucket: Optional[str] = None) -> str:
    bucket = explicit_bucket or os.getenv("S3_BUCKET") or os.getenv("AWS_S3_BUCKET")
    if not bucket:
        raise ValueError("Missing S3 bucket name. Set S3_BUCKET or AWS_S3_BUCKET.")
    return bucket


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY.")
    return api_key


def get_deepl_auth_key() -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing DEEPL_AUTH_KEY.")
    return auth_key


def get_cohere_api_key() -> str:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Missing COHERE_API_KEY.")
    return api_key
