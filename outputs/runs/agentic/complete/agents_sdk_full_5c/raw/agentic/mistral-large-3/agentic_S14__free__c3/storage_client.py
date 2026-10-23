import os
from typing import Optional

from google.cloud import storage


def get_storage_client() -> storage.Client:
    """
    Initialize and return a Google Cloud Storage client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    return storage.Client()


def get_bucket_name() -> str:
    """Return the configured bucket name from environment variable."""
    return os.environ["GCS_BUCKET_NAME"]