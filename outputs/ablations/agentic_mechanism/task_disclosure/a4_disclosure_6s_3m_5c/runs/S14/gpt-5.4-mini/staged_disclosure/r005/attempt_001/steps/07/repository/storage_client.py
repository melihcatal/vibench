import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config as BotoConfig
from botocore.client import BaseClient


@dataclass(frozen=True)
class ObjectStorageSettings:
    endpoint_url: Optional[str]
    region_name: str
    bucket_name: Optional[str]
    access_key_id: Optional[str]
    secret_access_key: Optional[str]
    session_token: Optional[str]
    use_ssl: bool
    signature_version: str


def load_object_storage_settings() -> ObjectStorageSettings:
    return ObjectStorageSettings(
        endpoint_url=os.getenv("OBJECT_STORAGE_ENDPOINT_URL") or os.getenv("S3_ENDPOINT_URL"),
        region_name=os.getenv("OBJECT_STORAGE_REGION", os.getenv("AWS_REGION", "us-east-1")),
        bucket_name=os.getenv("OBJECT_STORAGE_BUCKET") or os.getenv("S3_BUCKET"),
        access_key_id=os.getenv("OBJECT_STORAGE_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.getenv("OBJECT_STORAGE_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_ACCESS_KEY"),
        session_token=os.getenv("OBJECT_STORAGE_SESSION_TOKEN") or os.getenv("AWS_SESSION_TOKEN"),
        use_ssl=os.getenv("OBJECT_STORAGE_USE_SSL", "true").strip().lower() not in {"0", "false", "no"},
        signature_version=os.getenv("OBJECT_STORAGE_SIGNATURE_VERSION", "s3v4"),
    )


def build_boto_config(settings: Optional[ObjectStorageSettings] = None) -> BotoConfig:
    settings = settings or load_object_storage_settings()
    return BotoConfig(signature_version=settings.signature_version)


@lru_cache(maxsize=1)
def get_object_storage_client() -> BaseClient:
    settings = load_object_storage_settings()
    session = boto3.session.Session(
        aws_access_key_id=settings.access_key_id,
        aws_secret_access_key=settings.secret_access_key,
        aws_session_token=settings.session_token,
        region_name=settings.region_name,
    )
    return session.client(
        "s3",
        endpoint_url=settings.endpoint_url,
        use_ssl=settings.use_ssl,
        config=build_boto_config(settings),
    )


def get_bucket_name(default: Optional[str] = None) -> str:
    settings = load_object_storage_settings()
    bucket_name = settings.bucket_name or default
    if not bucket_name:
        raise ValueError("Object storage bucket name is not configured")
    return bucket_name


def reset_object_storage_client_cache() -> None:
    get_object_storage_client.cache_clear()
