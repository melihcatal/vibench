import os
from functools import lru_cache
from typing import Optional

from google.cloud import storage

from storage_models import StorageConfig


@lru_cache(maxsize=1)
def load_config() -> StorageConfig:
    return StorageConfig(
        bucket_name=os.environ["GCS_BUCKET_NAME"],
        project_id=os.getenv("GCP_PROJECT_ID"),
        credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        default_prefix=os.getenv("GCS_DEFAULT_PREFIX", ""),
    )


@lru_cache(maxsize=1)
def get_client() -> storage.Client:
    config = load_config()
    if config.credentials_path:
        return storage.Client.from_service_account_json(
            config.credentials_path, project=config.project_id
        )
    return storage.Client(project=config.project_id)


def get_bucket(bucket_name: Optional[str] = None):
    client = get_client()
    config = load_config()
    return client.bucket(bucket_name or config.bucket_name)
