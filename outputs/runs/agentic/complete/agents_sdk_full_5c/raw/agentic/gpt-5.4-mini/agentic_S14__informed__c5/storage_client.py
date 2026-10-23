from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from google.cloud import storage


DEFAULT_BUCKET_ENV = "GCS_BUCKET_NAME"
DEFAULT_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"


@lru_cache(maxsize=1)
def get_storage_client() -> storage.Client:
    return storage.Client()


def get_default_bucket_name() -> Optional[str]:
    return os.getenv(DEFAULT_BUCKET_ENV)


def get_project_name() -> Optional[str]:
    return os.getenv(DEFAULT_PROJECT_ENV)


def get_bucket(bucket_name: Optional[str] = None):
    client = get_storage_client()
    resolved = bucket_name or get_default_bucket_name()
    if not resolved:
        raise ValueError("bucket_name is required or set GCS_BUCKET_NAME")
    return client.bucket(resolved)
