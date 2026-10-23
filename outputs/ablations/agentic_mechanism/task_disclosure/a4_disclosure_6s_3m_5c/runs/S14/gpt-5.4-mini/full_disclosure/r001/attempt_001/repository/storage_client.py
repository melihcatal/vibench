import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config


@dataclass(frozen=True)
class StorageConfig:
    endpoint_url: Optional[str]
    region_name: str
    access_key_id: Optional[str]
    secret_access_key: Optional[str]
    session_token: Optional[str]
    bucket_name: Optional[str]
    use_ssl: bool
    signature_version: str


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def load_storage_config() -> StorageConfig:
    return StorageConfig(
        endpoint_url=_env("MANAGED_OBJECT_STORAGE_ENDPOINT_URL") or _env("AWS_ENDPOINT_URL"),
        region_name=_env("MANAGED_OBJECT_STORAGE_REGION", _env("AWS_REGION", "us-east-1")) or "us-east-1",
        access_key_id=_env("MANAGED_OBJECT_STORAGE_ACCESS_KEY_ID") or _env("AWS_ACCESS_KEY_ID"),
        secret_access_key=_env("MANAGED_OBJECT_STORAGE_SECRET_ACCESS_KEY") or _env("AWS_SECRET_ACCESS_KEY"),
        session_token=_env("MANAGED_OBJECT_STORAGE_SESSION_TOKEN") or _env("AWS_SESSION_TOKEN"),
        bucket_name=_env("MANAGED_OBJECT_STORAGE_BUCKET") or _env("AWS_S3_BUCKET"),
        use_ssl=(_env("MANAGED_OBJECT_STORAGE_USE_SSL", "true") or "true").lower() not in ("0", "false", "no"),
        signature_version=_env("MANAGED_OBJECT_STORAGE_SIGNATURE_VERSION", "s3v4") or "s3v4",
    )


def _client_kwargs(config: StorageConfig) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {
        "region_name": config.region_name,
        "use_ssl": config.use_ssl,
        "config": Config(signature_version=config.signature_version),
    }
    if config.endpoint_url:
        kwargs["endpoint_url"] = config.endpoint_url
    if config.access_key_id and config.secret_access_key:
        kwargs["aws_access_key_id"] = config.access_key_id
        kwargs["aws_secret_access_key"] = config.secret_access_key
    if config.session_token:
        kwargs["aws_session_token"] = config.session_token
    return kwargs


@lru_cache(maxsize=1)
def get_storage_config() -> StorageConfig:
    return load_storage_config()


@lru_cache(maxsize=1)
def get_storage_client():
    config = get_storage_config()
    return boto3.client("s3", **_client_kwargs(config))


def get_bucket_name(explicit_bucket: Optional[str] = None) -> str:
    bucket = explicit_bucket or get_storage_config().bucket_name
    if not bucket:
        raise ValueError("Bucket name is not configured")
    return bucket
