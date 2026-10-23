import os
from functools import lru_cache

from google.cloud import storage


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def storage_project_id() -> str:
    return _env("GOOGLE_CLOUD_PROJECT") or _env("GCP_PROJECT") or _env("GCLOUD_PROJECT")


@lru_cache(maxsize=1)
def get_storage_client() -> storage.Client:
    project = storage_project_id() or None
    return storage.Client(project=project)


def get_bucket(bucket_name: str):
    return get_storage_client().bucket(bucket_name)


def object_path(bucket: str, name: str) -> str:
    return f"gs://{bucket}/{name.lstrip('/')}"
