import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


@dataclass(frozen=True)
class SecretConfig:
    region_name: str
    secret_id: str
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None


def load_secret_config() -> SecretConfig:
    region_name = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    secret_id = os.getenv("SECRET_ID") or os.getenv("AWS_SECRET_ID") or ""
    if not secret_id:
        raise ValueError("Missing secret identifier: set SECRET_ID or AWS_SECRET_ID")
    return SecretConfig(
        region_name=region_name,
        secret_id=secret_id,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )


@lru_cache(maxsize=1)
def get_secrets_manager_client(config: Optional[SecretConfig] = None):
    cfg = config or load_secret_config()
    session = boto3.session.Session(
        aws_access_key_id=cfg.aws_access_key_id,
        aws_secret_access_key=cfg.aws_secret_access_key,
        aws_session_token=cfg.aws_session_token,
        region_name=cfg.region_name,
    )
    return session.client("secretsmanager")


def get_secret_string(secret_id: Optional[str] = None, config: Optional[SecretConfig] = None) -> str:
    cfg = config or load_secret_config()
    client = get_secrets_manager_client(cfg)
    response = client.get_secret_value(SecretId=secret_id or cfg.secret_id)
    secret_string = response.get("SecretString")
    if secret_string is not None:
        return secret_string
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        raise ValueError("Secret response did not include SecretString or SecretBinary")
    if isinstance(secret_binary, bytes):
        return secret_binary.decode("utf-8")
    return secret_binary


def get_secret_json(secret_id: Optional[str] = None, config: Optional[SecretConfig] = None) -> Dict[str, Any]:
    import json

    secret_value = get_secret_string(secret_id=secret_id, config=config)
    return json.loads(secret_value)


def put_secret_string(secret_value: str, secret_id: Optional[str] = None, config: Optional[SecretConfig] = None) -> Dict[str, Any]:
    cfg = config or load_secret_config()
    client = get_secrets_manager_client(cfg)
    return client.put_secret_value(SecretId=secret_id or cfg.secret_id, SecretString=secret_value)


def describe_secret(secret_id: Optional[str] = None, config: Optional[SecretConfig] = None) -> Dict[str, Any]:
    cfg = config or load_secret_config()
    client = get_secrets_manager_client(cfg)
    return client.describe_secret(SecretId=secret_id or cfg.secret_id)


def get_secret_value_safe(secret_id: Optional[str] = None, config: Optional[SecretConfig] = None) -> Optional[str]:
    try:
        return get_secret_string(secret_id=secret_id, config=config)
    except (ValueError, BotoCoreError, ClientError):
        return None
