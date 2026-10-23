import base64
import json
import os
from typing import Any, Optional

import boto3


def get_secret_manager_client(region_name: Optional[str] = None):
    region = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return boto3.session.Session(region_name=region).client("secretsmanager")


def get_secret_name(secret_name: Optional[str] = None) -> str:
    resolved = secret_name or os.getenv("AWS_SECRET_NAME") or os.getenv("SECRET_NAME") or os.getenv("DB_SECRET_NAME")
    if not resolved:
        raise ValueError("Missing secret name; set AWS_SECRET_NAME, SECRET_NAME, or DB_SECRET_NAME")
    return resolved


def fetch_secret_value(secret_name: Optional[str] = None, region_name: Optional[str] = None) -> str:
    client = get_secret_manager_client(region_name=region_name)
    response = client.get_secret_value(SecretId=get_secret_name(secret_name))
    secret_string = response.get("SecretString")
    if isinstance(secret_string, str) and secret_string:
        return secret_string
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        raise ValueError("Secret value is empty")
    if isinstance(secret_binary, bytes):
        return secret_binary.decode("utf-8")
    return base64.b64decode(secret_binary).decode("utf-8")


def fetch_secret_json(secret_name: Optional[str] = None, region_name: Optional[str] = None) -> dict[str, Any]:
    return json.loads(fetch_secret_value(secret_name=secret_name, region_name=region_name))


def get_client_config(prefix: str = "SECURITY", defaults: Optional[dict[str, str]] = None) -> dict[str, str]:
    defaults = defaults or {}
    config: dict[str, str] = {}
    for key, default in defaults.items():
        env_key = f"{prefix}_{key.upper()}"
        value = os.getenv(env_key, default)
        if value is not None:
            config[key] = value
    return config


class SecretClient:
    def __init__(self, secret_name: Optional[str] = None, region_name: Optional[str] = None):
        self.secret_name = secret_name
        self.region_name = region_name

    def get_text(self) -> str:
        return fetch_secret_value(secret_name=self.secret_name, region_name=self.region_name)

    def get_json(self) -> dict[str, Any]:
        return fetch_secret_json(secret_name=self.secret_name, region_name=self.region_name)
