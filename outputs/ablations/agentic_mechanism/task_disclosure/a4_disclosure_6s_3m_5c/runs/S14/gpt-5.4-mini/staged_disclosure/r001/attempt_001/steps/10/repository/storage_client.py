import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import Config


@dataclass(frozen=True)
class StorageConfig:
    bucket: str
    region: str
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None
    endpoint_url: Optional[str] = None


@lru_cache(maxsize=1)
def load_storage_config() -> StorageConfig:
    bucket = os.environ.get("AWS_S3_BUCKET") or os.environ.get("S3_BUCKET") or ""
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    session_token = os.environ.get("AWS_SESSION_TOKEN")
    endpoint_url = os.environ.get("S3_ENDPOINT_URL") or os.environ.get("AWS_S3_ENDPOINT_URL")
    return StorageConfig(
        bucket=bucket,
        region=region,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        session_token=session_token,
        endpoint_url=endpoint_url,
    )


@lru_cache(maxsize=1)
def get_s3_client():
    config = load_storage_config()
    client_kwargs = {
        "region_name": config.region,
        "config": Config(signature_version="s3v4"),
    }
    if config.access_key_id and config.secret_access_key:
        client_kwargs["aws_access_key_id"] = config.access_key_id
        client_kwargs["aws_secret_access_key"] = config.secret_access_key
    if config.session_token:
        client_kwargs["aws_session_token"] = config.session_token
    if config.endpoint_url:
        client_kwargs["endpoint_url"] = config.endpoint_url
    return boto3.client("s3", **client_kwargs)


def build_object_url(key: str, bucket: Optional[str] = None) -> str:
    config = load_storage_config()
    resolved_bucket = bucket or config.bucket
    if not resolved_bucket:
        raise ValueError("Storage bucket is not configured")
    return f"s3://{resolved_bucket}/{key.lstrip('/')}"


def get_bucket_name() -> str:
    bucket = load_storage_config().bucket
    if not bucket:
        raise ValueError("AWS_S3_BUCKET or S3_BUCKET must be set")
    return bucket


def client():
    return get_s3_client()
