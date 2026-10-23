from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.config import Config


DEFAULT_AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def get_aws_region(explicit_region: Optional[str] = None) -> str:
    return explicit_region or DEFAULT_AWS_REGION


def build_secrets_manager_client(region_name: Optional[str] = None):
    return boto3.client(
        "secretsmanager",
        region_name=get_aws_region(region_name),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def build_translate_client(region_name: Optional[str] = None):
    return boto3.client(
        "translate",
        region_name=get_aws_region(region_name),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value
