from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

DEFAULT_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
DEFAULT_SECRET_PREFIX = os.getenv("SECRET_ID_PREFIX", "")


@dataclass(frozen=True)
class SecretClientConfig:
    region_name: str = DEFAULT_REGION
    secret_id_prefix: str = DEFAULT_SECRET_PREFIX


def load_config() -> SecretClientConfig:
    return SecretClientConfig()


def client() -> Any:
    cfg = load_config()
    return boto3.client("secretsmanager", region_name=cfg.region_name, config=Config(retries={"max_attempts": 3}))


def secret_name(name: str) -> str:
    cfg = load_config()
    return f"{cfg.secret_id_prefix}{name}" if cfg.secret_id_prefix else name


def get_secret_value(secret_id: str, version_stage: Optional[str] = None, version_id: Optional[str] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {"SecretId": secret_name(secret_id)}
    if version_stage:
        params["VersionStage"] = version_stage
    if version_id:
        params["VersionId"] = version_id
    return client().get_secret_value(**params)


def parse_secret_payload(response: Dict[str, Any]) -> str:
    if "SecretString" in response and response["SecretString"] is not None:
        return response["SecretString"]
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        return ""
    if isinstance(secret_binary, (bytes, bytearray)):
        return secret_binary.decode("utf-8")
    return str(secret_binary)


def parse_json_secret(response: Dict[str, Any]) -> Dict[str, Any]:
    raw = parse_secret_payload(response)
    return json.loads(raw) if raw else {}


def safe_get_secret(secret_id: str, version_stage: Optional[str] = None, version_id: Optional[str] = None) -> Dict[str, Any]:
    try:
        return get_secret_value(secret_id, version_stage=version_stage, version_id=version_id)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Unable to fetch secret {secret_id}: {exc}") from exc


def normalize_secret_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "arn": response.get("ARN"),
        "name": response.get("Name"),
        "version_id": response.get("VersionId"),
        "stages": response.get("VersionStages", []),
        "created_date": response.get("CreatedDate"),
        "payload": parse_secret_payload(response),
    }
