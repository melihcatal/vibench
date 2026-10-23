import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass(frozen=True)
class StorageClientConfig:
    bucket: Optional[str] = None
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None


def load_storage_client_config() -> StorageClientConfig:
    return StorageClientConfig(
        bucket=os.environ.get("OBJECT_STORAGE_BUCKET"),
        region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"),
        access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        session_token=os.environ.get("AWS_SESSION_TOKEN"),
    )


def create_storage_client(config: Optional[StorageClientConfig] = None):
    cfg = config or load_storage_client_config()
    return boto3.client(
        "s3",
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        aws_session_token=cfg.session_token,
        region_name=cfg.region_name,
        endpoint_url=cfg.endpoint_url,
    )


def get_default_bucket(config: Optional[StorageClientConfig] = None) -> Optional[str]:
    cfg = config or load_storage_client_config()
    return cfg.bucket


def with_bucket(bucket: str, config: Optional[StorageClientConfig] = None) -> StorageClientConfig:
    cfg = config or load_storage_client_config()
    return StorageClientConfig(
        bucket=bucket,
        region_name=cfg.region_name,
        endpoint_url=cfg.endpoint_url,
        access_key_id=cfg.access_key_id,
        secret_access_key=cfg.secret_access_key,
        session_token=cfg.session_token,
    )
