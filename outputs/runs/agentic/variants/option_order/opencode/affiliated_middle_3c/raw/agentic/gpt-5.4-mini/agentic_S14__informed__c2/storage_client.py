import os
from functools import lru_cache
from google.cloud import storage


def get_project_id() -> str | None:
    return os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('GCLOUD_PROJECT')


@lru_cache(maxsize=1)
def get_client() -> storage.Client:
    return storage.Client(project=get_project_id())


def get_bucket(bucket_name: str):
    return get_client().bucket(bucket_name)
