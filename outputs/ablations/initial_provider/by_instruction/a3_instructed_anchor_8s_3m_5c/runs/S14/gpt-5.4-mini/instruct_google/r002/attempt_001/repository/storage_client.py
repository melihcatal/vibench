import os
from functools import lru_cache

from google.cloud import storage


@lru_cache(maxsize=1)
def get_storage_client() -> storage.Client:
    project = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    return storage.Client(project=project)


def get_storage_bucket_name(default: str = "") -> str:
    return os.environ.get("GCS_BUCKET", default)


def get_storage_object_name(default: str = "") -> str:
    return os.environ.get("GCS_OBJECT", default)
