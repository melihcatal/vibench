import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass(frozen=True)
class StorageConfig:
    bucket: str
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None


def load_storage_config(prefix: str = "S3_") -> StorageConfig:
    bucket = os.environ.get(f"{prefix}BUCKET") or os.environ.get("AWS_S3_BUCKET") or os.environ.get("S3_BUCKET")
    if not bucket:
        raise ValueError("storage bucket is required")
    return StorageConfig(
        bucket=bucket,
        region_name=os.environ.get(f"{prefix}REGION") or os.environ.get("AWS_REGION"),
        endpoint_url=os.environ.get(f"{prefix}ENDPOINT_URL") or os.environ.get("AWS_S3_ENDPOINT_URL"),
        access_key_id=os.environ.get(f"{prefix}ACCESS_KEY_ID") or os.environ.get("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.environ.get(f"{prefix}SECRET_ACCESS_KEY") or os.environ.get("AWS_SECRET_ACCESS_KEY"),
        session_token=os.environ.get(f"{prefix}SESSION_TOKEN") or os.environ.get("AWS_SESSION_TOKEN"),
    )


def create_storage_client(config: Optional[StorageConfig] = None):
    cfg = config or load_storage_config()
    return boto3.client(
        "s3",
        region_name=cfg.region_name,
        endpoint_url=cfg.endpoint_url,
        aws_access_key_id=cfg.access_key_id,
        aws_secret_access_key=cfg.secret_access_key,
        aws_session_token=cfg.session_token,
    )


def get_bucket_name(config: Optional[StorageConfig] = None) -> str:
    return (config or load_storage_config()).bucket
