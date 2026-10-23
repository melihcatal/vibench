from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_secret_manager_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("secretsmanager", region_name=region_name or get_aws_region())


def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key


def get_perspective_api_key() -> str:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    return api_key


def get_deepl_api_key() -> str:
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    return api_key
