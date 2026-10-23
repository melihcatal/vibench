from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import boto3
from botocore.client import BaseClient

DEFAULT_AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DEFAULT_SECRET_ID = os.getenv("SECRET_ID", "example/secret")
DEFAULT_SM_CLIENT_VERSION_STAGE = os.getenv("SECRET_VERSION_STAGE", "AWSCURRENT")


@dataclass(frozen=True)
class SecretRequestConfig:
    secret_id: str = DEFAULT_SECRET_ID
    region_name: str = DEFAULT_AWS_REGION
    version_stage: str = DEFAULT_SM_CLIENT_VERSION_STAGE
    version_id: Optional[str] = None


def load_config(secret_id: Optional[str] = None, region_name: Optional[str] = None, version_stage: Optional[str] = None, version_id: Optional[str] = None) -> SecretRequestConfig:
    return SecretRequestConfig(
        secret_id=secret_id or DEFAULT_SECRET_ID,
        region_name=region_name or DEFAULT_AWS_REGION,
        version_stage=version_stage or DEFAULT_SM_CLIENT_VERSION_STAGE,
        version_id=version_id,
    )


def make_secrets_client(region_name: Optional[str] = None) -> BaseClient:
    return boto3.client("secretsmanager", region_name=region_name or DEFAULT_AWS_REGION)


def get_secret_value(secret_id: str, region_name: Optional[str] = None, version_stage: Optional[str] = None, version_id: Optional[str] = None):
    client = make_secrets_client(region_name)
    request = {"SecretId": secret_id}
    if version_stage:
        request["VersionStage"] = version_stage
    if version_id:
        request["VersionId"] = version_id
    return client.get_secret_value(**request)
