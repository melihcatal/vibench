import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3


@dataclass(frozen=True)
class ManagedObjectStorageConfig:
    access_key_id: Optional[str]
    secret_access_key: Optional[str]
    session_token: Optional[str]
    region_name: Optional[str]
    endpoint_url: Optional[str]
    profile_name: Optional[str]


def load_config() -> ManagedObjectStorageConfig:
    return ManagedObjectStorageConfig(
        access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        endpoint_url=os.getenv("AWS_ENDPOINT_URL") or os.getenv("S3_ENDPOINT_URL"),
        profile_name=os.getenv("AWS_PROFILE"),
    )


@lru_cache(maxsize=1)
def get_client():
    config = load_config()
    session_kwargs = {}
    if config.profile_name:
        session_kwargs["profile_name"] = config.profile_name
    session = boto3.Session(**session_kwargs)
    client_kwargs = {}
    if config.access_key_id:
        client_kwargs["aws_access_key_id"] = config.access_key_id
    if config.secret_access_key:
        client_kwargs["aws_secret_access_key"] = config.secret_access_key
    if config.session_token:
        client_kwargs["aws_session_token"] = config.session_token
    if config.region_name:
        client_kwargs["region_name"] = config.region_name
    if config.endpoint_url:
        client_kwargs["endpoint_url"] = config.endpoint_url
    return session.client("s3", **client_kwargs)


def reset_client_cache() -> None:
    get_client.cache_clear()


def get_bucket_location(bucket: str):
    return get_client().get_bucket_location(Bucket=bucket)


def build_s3_uri(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key}"


__all__ = ["ManagedObjectStorageConfig", "build_s3_uri", "get_bucket_location", "get_client", "load_config", "reset_client_cache"]
