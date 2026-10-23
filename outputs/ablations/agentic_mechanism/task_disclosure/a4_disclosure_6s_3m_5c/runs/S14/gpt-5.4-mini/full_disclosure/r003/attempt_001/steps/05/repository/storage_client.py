import os
from dataclasses import dataclass
from typing import Any, Optional

import boto3


def _env(name: str, fallback: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else fallback


@dataclass(frozen=True)
class StorageConfig:
    endpoint_url: Optional[str] = None
    region_name: Optional[str] = None
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None
    signature_version: Optional[str] = None

    @classmethod
    def from_env(cls) -> "StorageConfig":
        return cls(
            endpoint_url=_env("AWS_S3_ENDPOINT_URL") or _env("AWS_ENDPOINT_URL"),
            region_name=_env("AWS_REGION") or _env("AWS_DEFAULT_REGION"),
            access_key_id=_env("AWS_ACCESS_KEY_ID"),
            secret_access_key=_env("AWS_SECRET_ACCESS_KEY"),
            session_token=_env("AWS_SESSION_TOKEN"),
            signature_version=_env("AWS_S3_SIGNATURE_VERSION"),
        )


def get_storage_config() -> StorageConfig:
    return StorageConfig.from_env()


def create_storage_session(config: Optional[StorageConfig] = None) -> boto3.session.Session:
    cfg = config or get_storage_config()
    return boto3.session.Session(
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        aws_session_token=cfg.session_token,
        region_name=cfg.region_name,
    )


def create_storage_client(config: Optional[StorageConfig] = None) -> Any:
    cfg = config or get_storage_config()
    session = create_storage_session(cfg)
    client_kwargs: dict[str, Any] = {}
    if cfg.endpoint_url:
        client_kwargs["endpoint_url"] = cfg.endpoint_url
    if cfg.signature_version:
        from botocore.config import Config

        client_kwargs["config"] = Config(signature_version=cfg.signature_version)
    return session.client("s3", **client_kwargs)


def resolve_bucket_name(bucket: Optional[str] = None) -> str:
    resolved = bucket or _env("S3_BUCKET") or _env("BUCKET")
    if not resolved:
        raise ValueError("bucket name is required")
    return resolved


def resolve_object_key(object_key: Optional[str] = None) -> str:
    resolved = object_key or _env("S3_OBJECT_KEY") or _env("OBJECT_KEY")
    if not resolved:
        raise ValueError("object key is required")
    return resolved
