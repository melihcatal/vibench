from google.cloud import storage
import os


def get_storage_client() -> storage.Client:
    """Initializes and returns a Google Cloud Storage client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return storage.Client()


def get_bucket(bucket_name: str) -> storage.Bucket:
    """Returns a Google Cloud Storage bucket object."""
    client = get_storage_client()
    return client.bucket(bucket_name)
