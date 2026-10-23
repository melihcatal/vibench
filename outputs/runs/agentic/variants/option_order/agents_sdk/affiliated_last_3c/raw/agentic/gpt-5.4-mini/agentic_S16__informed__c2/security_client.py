from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_models import SecretRequest, SecretResponse, normalize_secret_value, parse_json_maybe

AWS_REGION_ENV = "AWS_REGION"
AWS_PROFILE_ENV = "AWS_PROFILE"
DEFAULT_SECRETS_MANAGER_ENDPOINT = "secretsmanager.us-east-1.amazonaws.com"


@dataclass(frozen=True)
class SecurityClientConfig:
    region_name: str
    endpoint_url: Optional[str] = None


@lru_cache(maxsize=1)
def load_config() -> SecurityClientConfig:
    return SecurityClientConfig(
        region_name=os.getenv(AWS_REGION_ENV, "us-east-1"),
        endpoint_url=os.getenv("AWS_SECRETS_MANAGER_ENDPOINT", f"https://{DEFAULT_SECRETS_MANAGER_ENDPOINT}"),
    )


@lru_cache(maxsize=1)
def secretsmanager_client():
    config = load_config()
    session_kwargs: Dict[str, Any] = {}
    profile = os.getenv(AWS_PROFILE_ENV)
    if profile:
        session_kwargs["profile_name"] = profile
    session = boto3.Session(**session_kwargs)
    return session.client("secretsmanager", region_name=config.region_name, endpoint_url=config.endpoint_url)


def fetch_secret_string(secret_id: str, version: Optional[str] = None, stage: Optional[str] = None) -> SecretResponse:
    client = secretsmanager_client()
    kwargs: Dict[str, Any] = {"SecretId": secret_id}
    if version:
        kwargs["VersionId"] = version
    if stage:
        kwargs["VersionStage"] = stage
    try:
        payload = client.get_secret_value(**kwargs)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Unable to fetch secret {secret_id!r}: {exc}") from exc

    secret_value = payload.get("SecretString")
    if secret_value is None and payload.get("SecretBinary") is not None:
        secret_value = payload["SecretBinary"]
    return SecretResponse(
        secret_id=secret_id,
        version=payload.get("VersionId"),
        value=normalize_secret_value(secret_value),
        metadata={k: v for k, v in payload.items() if k not in {"SecretString", "SecretBinary"}},
    )


def fetch_secret_json(secret_id: str, version: Optional[str] = None, stage: Optional[str] = None) -> Dict[str, Any]:
    response = fetch_secret_string(secret_id=secret_id, version=version, stage=stage)
    return parse_json_maybe(response.value)


def fetch_by_request(request: SecretRequest) -> SecretResponse:
    return fetch_secret_string(request.secret_id, version=request.version, stage=request.stage)
