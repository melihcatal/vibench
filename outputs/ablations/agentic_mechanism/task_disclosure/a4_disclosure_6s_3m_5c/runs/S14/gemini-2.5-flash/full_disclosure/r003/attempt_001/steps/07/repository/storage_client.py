
import os
from google.cloud import storage

def get_storage_client():
    """
    Provides a Google Cloud Storage client.
    """
    return storage.Client()

def get_bucket_name():
    """
    Retrieves the Google Cloud Storage bucket name from environment variables.
    """
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")
    return bucket_name
