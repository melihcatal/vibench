from __future__ import annotations

import os
from typing import Optional

import boto3


def aws_region(default: str = "us-east-1") -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or default


def secrets_manager_client(region_name: Optional[str] = None):
    return boto3.client("secretsmanager", region_name=region_name or aws_region())


def bedrock_runtime_client(region_name: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region_name or aws_region())


def translate_client(region_name: Optional[str] = None):
    return boto3.client("translate", region_name=region_name or aws_region())


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value
