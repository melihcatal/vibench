import os
from typing import Optional

from google.cloud import storage


def get_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def get_bucket_name() -> Optional[str]:
    return os.getenv("GCS_BUCKET") or os.getenv("GOOGLE_STORAGE_BUCKET")


def get_storage_client() -> storage.Client:
    return storage.Client(project=get_project_id())


def get_bucket(bucket_name: Optional[str] = None) -> storage.Bucket:
    client = get_storage_client()
    resolved_bucket = bucket_name or get_bucket_name()
    if not resolved_bucket:
        raise ValueError("Missing bucket name")
    return client.bucket(resolved_bucket)


def get_object_path(key: str) -> str:
    return key.lstrip("/")
