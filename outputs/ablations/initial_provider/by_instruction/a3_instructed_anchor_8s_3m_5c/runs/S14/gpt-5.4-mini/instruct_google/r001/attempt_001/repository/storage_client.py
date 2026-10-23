import os
from functools import lru_cache
from typing import Optional

from google.cloud import storage


def get_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


@lru_cache(maxsize=1)
def get_storage_client() -> storage.Client:
    return storage.Client(project=get_project_id())


def get_bucket(bucket_name: str):
    return get_storage_client().bucket(bucket_name)
