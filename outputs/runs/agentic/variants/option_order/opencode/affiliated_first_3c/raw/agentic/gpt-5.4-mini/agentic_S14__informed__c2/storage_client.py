import os
from dataclasses import dataclass
from functools import lru_cache

from boto3.session import Session


@dataclass(frozen=True)
class StorageConfig:
    bucket: str
    region_name: str | None
    endpoint_url: str | None


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value if value else None


@lru_cache(maxsize=1)
def get_storage_config() -> StorageConfig:
    return StorageConfig(
        bucket=_env("OBJECT_STORAGE_BUCKET", "managed-object-storage")
        or "managed-object-storage",
        region_name=_env("AWS_REGION") or _env("AWS_DEFAULT_REGION"),
        endpoint_url=_env("AWS_ENDPOINT_URL"),
    )


@lru_cache(maxsize=1)
def get_s3_client():
    config = get_storage_config()
    session = Session()
    return session.client(
        "s3", region_name=config.region_name, endpoint_url=config.endpoint_url
    )


def get_bucket_name() -> str:
    return get_storage_config().bucket
