import os
from dataclasses import dataclass

from google.cloud import storage


@dataclass
class StorageConfig:
    bucket_name: str


def load_storage_config() -> StorageConfig:
    bucket_name = os.environ.get("GCS_BUCKET_NAME") or os.environ.get(
        "STORAGE_BUCKET_NAME"
    )
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME is required")
    return StorageConfig(bucket_name=bucket_name)


def get_storage_client() -> storage.Client:
    return storage.Client()


def get_bucket(client: storage.Client, bucket_name: str):
    return client.bucket(bucket_name)
