import os
from google.cloud import storage

def get_storage_client():
    """
    Initializes and returns a Google Cloud Storage client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return storage.Client()

def get_default_bucket_name():
    """
    Returns the default GCS bucket name from an environment variable.
    """
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")
    return bucket_name
