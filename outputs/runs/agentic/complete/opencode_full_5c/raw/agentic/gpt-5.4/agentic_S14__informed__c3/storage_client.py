from __future__ import annotations

import os

import boto3
from botocore.client import BaseClient


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_s3_client() -> BaseClient:
    return boto3.client("s3", region_name=get_aws_region())


def get_textract_client() -> BaseClient:
    return boto3.client("textract", region_name=get_aws_region())


def require_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key


def require_deepl_auth_key() -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    return auth_key
