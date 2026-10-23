import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config


@dataclass(frozen=True)
class SecretManagementConfig:
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    profile_name: Optional[str] = None
    retries: Dict[str, Any] = field(default_factory=lambda: {"max_attempts": 3, "mode": "standard"})
    connect_timeout: int = 5
    read_timeout: int = 10

    @classmethod
    def from_env(cls) -> "SecretManagementConfig":
        return cls(
            region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
            endpoint_url=os.getenv("AWS_SECRETS_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
            profile_name=os.getenv("AWS_PROFILE"),
        )


def load_secret_management_config() -> SecretManagementConfig:
    return SecretManagementConfig.from_env()


def create_secretsmanager_client(config: Optional[SecretManagementConfig] = None):
    cfg = config or load_secret_management_config()
    boto_config = Config(
        retries=cfg.retries,
        connect_timeout=cfg.connect_timeout,
        read_timeout=cfg.read_timeout,
    )
    session_kwargs: Dict[str, Any] = {}
    if cfg.profile_name:
        session_kwargs["profile_name"] = cfg.profile_name
    session = boto3.Session(**session_kwargs)
    client_kwargs: Dict[str, Any] = {"config": boto_config}
    if cfg.region_name:
        client_kwargs["region_name"] = cfg.region_name
    if cfg.endpoint_url:
        client_kwargs["endpoint_url"] = cfg.endpoint_url
    if cfg.aws_access_key_id and cfg.aws_secret_access_key:
        client_kwargs["aws_access_key_id"] = cfg.aws_access_key_id
        client_kwargs["aws_secret_access_key"] = cfg.aws_secret_access_key
    if cfg.aws_session_token:
        client_kwargs["aws_session_token"] = cfg.aws_session_token
    return session.client("secretsmanager", **client_kwargs)


def get_secret_string(secret_id: str, version_stage: Optional[str] = None, version_id: Optional[str] = None, config: Optional[SecretManagementConfig] = None) -> str:
    client = create_secretsmanager_client(config)
    params: Dict[str, Any] = {"SecretId": secret_id}
    if version_stage:
        params["VersionStage"] = version_stage
    if version_id:
        params["VersionId"] = version_id
    response = client.get_secret_value(**params)
    secret_string = response.get("SecretString")
    if secret_string is None:
        secret_binary = response.get("SecretBinary")
        if secret_binary is not None:
            return secret_binary.decode("utf-8") if hasattr(secret_binary, "decode") else str(secret_binary)
        return ""
    return secret_string


def get_secret_payload(secret_id: str, version_stage: Optional[str] = None, version_id: Optional[str] = None, config: Optional[SecretManagementConfig] = None) -> Dict[str, Any]:
    client = create_secretsmanager_client(config)
    params: Dict[str, Any] = {"SecretId": secret_id}
    if version_stage:
        params["VersionStage"] = version_stage
    if version_id:
        params["VersionId"] = version_id
    return client.get_secret_value(**params)
