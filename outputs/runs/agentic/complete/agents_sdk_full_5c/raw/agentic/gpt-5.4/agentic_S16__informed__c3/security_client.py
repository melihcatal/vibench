from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient


DEFAULT_AWS_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_secrets_manager_client(region_name: Optional[str] = None) -> BaseClient:
    session = boto3.session.Session(region_name=region_name or DEFAULT_AWS_REGION)
    return session.client("secretsmanager")


def require_secret_id(env_name: str, default: Optional[str] = None) -> str:
    value = os.getenv(env_name, default)
    if not value:
        raise ValueError(f"Missing required secret identifier in environment variable: {env_name}")
    return value


def optional_version_id(env_name: str = "SECRET_VERSION_ID") -> Optional[str]:
    return os.getenv(env_name) or None


def optional_version_stage(env_name: str = "SECRET_VERSION_STAGE", default: Optional[str] = None) -> Optional[str]:
    return os.getenv(env_name, default) or None
