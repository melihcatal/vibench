from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.client import BaseClient


DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def get_secrets_manager_client(region_name: Optional[str] = None) -> BaseClient:
    session = boto3.session.Session(region_name=region_name or DEFAULT_REGION)
    return session.client("secretsmanager")


def require_secret_id(env_var: str, default: Optional[str] = None) -> str:
    value = os.getenv(env_var, default)
    if not value:
        raise ValueError(f"Missing required secret identifier in environment variable: {env_var}")
    return value


def decode_secret_value(response: dict) -> str:
    if "SecretString" in response and response["SecretString"] is not None:
        return response["SecretString"]
    if "SecretBinary" in response and response["SecretBinary"] is not None:
        binary_value = response["SecretBinary"]
        if isinstance(binary_value, (bytes, bytearray)):
            return binary_value.decode("utf-8")
        return str(binary_value)
    raise ValueError("AWS Secrets Manager response did not contain SecretString or SecretBinary")
