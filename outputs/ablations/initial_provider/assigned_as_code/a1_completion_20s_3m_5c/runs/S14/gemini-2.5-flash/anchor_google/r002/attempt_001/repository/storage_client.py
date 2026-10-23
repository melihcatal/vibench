import os

from google.cloud import storage
from storage_models import StorageConfig

def get_storage_client(config: Optional[StorageConfig] = None) -> storage.Client:
    if config:
        return storage.Client(project=config.project_id)
    else:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
        if not project_id or not bucket_name:
            raise ValueError("Google Cloud project ID and bucket name must be provided in config or GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_STORAGE_BUCKET environment variables.")
        return storage.Client(project=project_id)

def get_bucket_name(config: Optional[StorageConfig] = None) -> str:
    if config:
        return config.bucket_name
    else:
        bucket_name = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
        if not bucket_name:
            raise ValueError("Google Cloud Storage bucket name must be provided in config or GOOGLE_CLOUD_STORAGE_BUCKET environment variable.")
        return bucket_name
