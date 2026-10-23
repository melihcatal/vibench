import os
from dataclasses import dataclass
from functools import lru_cache

from google.cloud import storage


@dataclass(frozen=True)
class StorageConfig:
    project: str | None
    bucket: str | None


def load_config() -> StorageConfig:
    return StorageConfig(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"), bucket=os.getenv("STORAGE_BUCKET")
    )


@lru_cache(maxsize=1)
def get_client() -> storage.Client:
    return storage.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))


def get_bucket_name(explicit_bucket: str | None = None) -> str:
    bucket = explicit_bucket or os.getenv("STORAGE_BUCKET")
    if not bucket:
        raise ValueError("bucket is required")
    return bucket
