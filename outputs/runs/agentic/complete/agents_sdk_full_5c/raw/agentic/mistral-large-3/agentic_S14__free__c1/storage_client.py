import os
from typing import Optional

from google.cloud import storage


def get_storage_client() -> storage.Client:
    """
    Initialize and return a Google Cloud Storage client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
    """
    return storage.Client()


def get_bucket_name() -> str:
    """Return the Google Cloud Storage bucket name from environment variable."""
    return os.environ["GCS_BUCKET_NAME"]