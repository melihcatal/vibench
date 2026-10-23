import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config as BotoConfig


@dataclass(frozen=True)
class SecretManagementConfig:
    region_name: str
    secrets_manager_endpoint_url: Optional[str] = None
    session_token: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None


def load_config() -> SecretManagementConfig:
    return SecretManagementConfig(
        region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1",
        secrets_manager_endpoint_url=os.environ.get("AWS_SECRETS_MANAGER_ENDPOINT_URL"),
        session_token=os.environ.get("AWS_SESSION_TOKEN"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


@lru_cache(maxsize=1)
def get_secrets_manager_client() -> Any:
    config = load_config()
    session = boto3.session.Session(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.session_token,
        region_name=config.region_name,
    )
    return session.client(
        "secretsmanager",
        endpoint_url=config.secrets_manager_endpoint_url,
        config=BotoConfig(retries={"max_attempts": 3, "mode": "standard"}),
    )


def normalize_secret_string(secret_value: Any) -> str:
    if secret_value is None:
        return ""
    if isinstance(secret_value, bytes):
        return secret_value.decode("utf-8")
    return str(secret_value)


def secret_string_from_response(response: Dict[str, Any]) -> str:
    if "SecretString" in response and response["SecretString"] is not None:
        return normalize_secret_string(response["SecretString"])
    if "SecretBinary" in response and response["SecretBinary"] is not None:
        return normalize_secret_string(response["SecretBinary"])
    return ""
