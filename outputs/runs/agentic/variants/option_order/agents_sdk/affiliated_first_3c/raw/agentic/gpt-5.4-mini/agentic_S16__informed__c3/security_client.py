from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from security_models import NormalizedSecret, SecretName, SecretPayload, coerce_mapping

AWS_REGION_ENV = "AWS_REGION"
AWS_SECRET_ID_ENV = "SECURITY_SECRET_ID"
AWS_SECRET_VERSION_ENV = "SECURITY_SECRET_VERSION"
AWS_SECRET_STAGE_ENV = "SECURITY_SECRET_STAGE"


@lru_cache(maxsize=1)
def get_secrets_manager_client(region_name: Optional[str] = None):
    region = region_name or os.getenv(AWS_REGION_ENV) or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client("secretsmanager", region_name=region, config=Config(retries={"max_attempts": 3}))


def _get_secret_string(client, secret_id: str, version_id: str | None = None, version_stage: str | None = None) -> str:
    kwargs: dict[str, Any] = {"SecretId": secret_id}
    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage:
        kwargs["VersionStage"] = version_stage
    response = client.get_secret_value(**kwargs)
    if "SecretString" in response and response["SecretString"] is not None:
        return response["SecretString"]
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        return ""
    return secret_binary.decode("utf-8") if hasattr(secret_binary, "decode") else str(secret_binary)


def fetch_secret_payload(secret_id: str, *, version_id: str | None = None, version_stage: str | None = None, region_name: str | None = None) -> SecretPayload:
    client = get_secrets_manager_client(region_name)
    text = _get_secret_string(client, secret_id, version_id=version_id, version_stage=version_stage)
    response = SecretPayload(name=secret_id, value=text, version=version_id or version_stage)
    return response


def fetch_json_secret(secret_id: str, *, version_id: str | None = None, version_stage: str | None = None, region_name: str | None = None) -> NormalizedSecret:
    payload = fetch_secret_payload(secret_id, version_id=version_id, version_stage=version_stage, region_name=region_name)
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        parsed = None
    return NormalizedSecret(name=payload.name, text=payload.value, parsed_json=coerce_mapping(parsed) if isinstance(parsed, dict) else None)


def env_secret_name(default: str = "") -> SecretName:
    return SecretName(os.getenv(AWS_SECRET_ID_ENV, default))


def env_secret_version() -> tuple[Optional[str], Optional[str]]:
    return os.getenv(AWS_SECRET_VERSION_ENV), os.getenv(AWS_SECRET_STAGE_ENV)


def safe_fetch(secret_id: str, *, version_id: str | None = None, version_stage: str | None = None, region_name: str | None = None) -> str:
    try:
        return fetch_secret_payload(secret_id, version_id=version_id, version_stage=version_stage, region_name=region_name).value
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"AWS Secrets Manager lookup failed for {secret_id}: {exc}") from exc
