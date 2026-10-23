from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import storage as gcs_storage


@dataclass(frozen=True)
class StorageConfig:
    bucket: str
    project: Optional[str] = None
    credentials_path: Optional[str] = None


@lru_cache(maxsize=1)
def get_storage_config() -> StorageConfig:
    bucket = os.environ.get("GCS_BUCKET", "")
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    return StorageConfig(bucket=bucket, project=project, credentials_path=credentials_path)


@lru_cache(maxsize=1)
def get_storage_client() -> gcs_storage.Client:
    cfg = get_storage_config()
    return gcs_storage.Client(project=cfg.project)


def get_bucket(bucket_name: Optional[str] = None):
    client = get_storage_client()
    name = bucket_name or get_storage_config().bucket
    if not name:
        raise ValueError("Bucket name is required via argument or GCS_BUCKET")
    return client.bucket(name)
