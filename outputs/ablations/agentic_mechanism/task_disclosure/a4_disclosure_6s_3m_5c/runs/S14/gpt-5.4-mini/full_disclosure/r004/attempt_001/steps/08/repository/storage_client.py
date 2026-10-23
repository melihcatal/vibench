import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config


DEFAULT_REGION_ENV_VARS = ("AWS_REGION", "AWS_DEFAULT_REGION")


@dataclass
class ManagedObjectStorageConfig:
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None
    profile_name: Optional[str] = None
    signature_version: Optional[str] = None
    max_pool_connections: int = 10
    retries_max_attempts: int = 5
    retries_mode: str = "standard"
    connect_timeout: int = 10
    read_timeout: int = 60
    verify: Optional[bool] = None


def _env_first(*names: str) -> Optional[str]:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def load_managed_object_storage_config(overrides: Optional[Dict[str, Any]] = None) -> ManagedObjectStorageConfig:
    overrides = overrides or {}
    region_name = overrides.get("region_name") or _env_first(*DEFAULT_REGION_ENV_VARS)
    endpoint_url = overrides.get("endpoint_url") or _env_first("MANAGED_OBJECT_STORAGE_ENDPOINT_URL", "AWS_ENDPOINT_URL")
    access_key_id = overrides.get("access_key_id") or _env_first("MANAGED_OBJECT_STORAGE_ACCESS_KEY_ID", "AWS_ACCESS_KEY_ID")
    secret_access_key = overrides.get("secret_access_key") or _env_first("MANAGED_OBJECT_STORAGE_SECRET_ACCESS_KEY", "AWS_SECRET_ACCESS_KEY")
    session_token = overrides.get("session_token") or _env_first("MANAGED_OBJECT_STORAGE_SESSION_TOKEN", "AWS_SESSION_TOKEN")
    profile_name = overrides.get("profile_name") or _env_first("AWS_PROFILE")
    signature_version = overrides.get("signature_version") or _env_first("MANAGED_OBJECT_STORAGE_SIGNATURE_VERSION")
    max_pool_connections = int(overrides.get("max_pool_connections") or os.getenv("MANAGED_OBJECT_STORAGE_MAX_POOL_CONNECTIONS", "10"))
    retries_max_attempts = int(overrides.get("retries_max_attempts") or os.getenv("MANAGED_OBJECT_STORAGE_RETRIES_MAX_ATTEMPTS", "5"))
    retries_mode = str(overrides.get("retries_mode") or os.getenv("MANAGED_OBJECT_STORAGE_RETRIES_MODE", "standard"))
    connect_timeout = int(overrides.get("connect_timeout") or os.getenv("MANAGED_OBJECT_STORAGE_CONNECT_TIMEOUT", "10"))
    read_timeout = int(overrides.get("read_timeout") or os.getenv("MANAGED_OBJECT_STORAGE_READ_TIMEOUT", "60"))
    verify = overrides.get("verify")
    if verify is None:
        verify_env = os.getenv("MANAGED_OBJECT_STORAGE_VERIFY")
        if verify_env is not None:
            verify = verify_env.lower() not in {"0", "false", "no"}
    return ManagedObjectStorageConfig(
        region_name=region_name,
        endpoint_url=endpoint_url,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        session_token=session_token,
        profile_name=profile_name,
        signature_version=signature_version,
        max_pool_connections=max_pool_connections,
        retries_max_attempts=retries_max_attempts,
        retries_mode=retries_mode,
        connect_timeout=connect_timeout,
        read_timeout=read_timeout,
        verify=verify,
    )


def build_boto3_session(config: Optional[ManagedObjectStorageConfig] = None):
    config = config or load_managed_object_storage_config()
    session_kwargs: Dict[str, Any] = {}
    if config.profile_name:
        session_kwargs["profile_name"] = config.profile_name
    if config.region_name:
        session_kwargs["region_name"] = config.region_name
    if config.access_key_id and config.secret_access_key:
        session_kwargs["aws_access_key_id"] = config.access_key_id
        session_kwargs["aws_secret_access_key"] = config.secret_access_key
    if config.session_token:
        session_kwargs["aws_session_token"] = config.session_token
    return boto3.Session(**session_kwargs)


def build_boto_config(config: Optional[ManagedObjectStorageConfig] = None) -> Config:
    config = config or load_managed_object_storage_config()
    client_config: Dict[str, Any] = {
        "connect_timeout": config.connect_timeout,
        "read_timeout": config.read_timeout,
        "max_pool_connections": config.max_pool_connections,
        "retries": {"max_attempts": config.retries_max_attempts, "mode": config.retries_mode},
    }
    if config.signature_version:
        client_config["signature_version"] = config.signature_version
    return Config(**client_config)


def build_managed_object_storage_client(service_name: str = "s3", config: Optional[ManagedObjectStorageConfig] = None):
    config = config or load_managed_object_storage_config()
    session = build_boto3_session(config)
    client_kwargs: Dict[str, Any] = {"config": build_boto_config(config)}
    if config.region_name:
        client_kwargs["region_name"] = config.region_name
    if config.endpoint_url:
        client_kwargs["endpoint_url"] = config.endpoint_url
    if config.verify is not None:
        client_kwargs["verify"] = config.verify
    return session.client(service_name, **client_kwargs)


def resolve_managed_object_storage_bucket(default_bucket: Optional[str] = None) -> Optional[str]:
    return default_bucket or _env_first("MANAGED_OBJECT_STORAGE_BUCKET", "AWS_S3_BUCKET", "S3_BUCKET")


def resolve_managed_object_storage_prefix(default_prefix: str = "") -> str:
    return os.getenv("MANAGED_OBJECT_STORAGE_PREFIX", default_prefix)
