import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import storage
from google.oauth2 import service_account


@dataclass(frozen=True)
class StorageConfig:
    project_id: Optional[str]
    credentials_json: Optional[str]
    service_account_file: Optional[str]


def load_config() -> StorageConfig:
    return StorageConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        credentials_json=os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"),
        service_account_file=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    )


@lru_cache(maxsize=1)
def get_storage_client() -> storage.Client:
    config = load_config()
    if config.credentials_json:
        credentials = service_account.Credentials.from_service_account_info(__import__("json").loads(config.credentials_json))
        return storage.Client(project=config.project_id, credentials=credentials)
    if config.service_account_file:
        return storage.Client.from_service_account_json(config.service_account_file, project=config.project_id)
    return storage.Client(project=config.project_id)


def get_bucket(bucket_name: str) -> storage.Bucket:
    return get_storage_client().bucket(bucket_name)
