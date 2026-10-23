from __future__ import annotations

import os
from typing import Optional

import boto3

from security_models import SecretPayload


AWS_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def build_secrets_manager_client(region_name: Optional[str] = None):
    return boto3.client("secretsmanager", region_name=region_name or AWS_REGION)


def fetch_secret_payload(secret_id: str, *, version_id: Optional[str] = None, version_stage: Optional[str] = None, region_name: Optional[str] = None) -> SecretPayload:
    client = build_secrets_manager_client(region_name=region_name)
    params = {"SecretId": secret_id}
    if version_id:
        params["VersionId"] = version_id
    if version_stage:
        params["VersionStage"] = version_stage
    response = client.get_secret_value(**params)
    value = response.get("SecretString")
    if value is None and response.get("SecretBinary") is not None:
        binary_value = response["SecretBinary"]
        value = binary_value.decode("utf-8") if isinstance(binary_value, bytes) else str(binary_value)
    if value is None:
        raise ValueError("Unable to extract secret value from AWS Secrets Manager response")
    return SecretPayload(
        secret_id=secret_id,
        version_id=response.get("VersionId"),
        version_stages=tuple(response.get("VersionStages", [])),
        value=value,
    )


def describe_secret(secret_id: str, *, region_name: Optional[str] = None):
    client = build_secrets_manager_client(region_name=region_name)
    return client.describe_secret(SecretId=secret_id)
