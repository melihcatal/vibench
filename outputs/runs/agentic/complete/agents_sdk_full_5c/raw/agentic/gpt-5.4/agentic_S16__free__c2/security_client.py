from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient


DEFAULT_AWS_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
DEFAULT_BEDROCK_REGION = os.getenv("BEDROCK_REGION") or DEFAULT_AWS_REGION
DEFAULT_SECRET_PREFIX = os.getenv("SECRET_NAME_PREFIX", "app/")


def build_secret_name(name: str) -> str:
    if name.startswith(DEFAULT_SECRET_PREFIX):
        return name
    return f"{DEFAULT_SECRET_PREFIX}{name}"


def get_secrets_manager_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("secretsmanager", region_name=region_name or DEFAULT_AWS_REGION)


def get_bedrock_runtime_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("bedrock-runtime", region_name=region_name or DEFAULT_BEDROCK_REGION)


def get_translate_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("translate", region_name=region_name or DEFAULT_AWS_REGION)
