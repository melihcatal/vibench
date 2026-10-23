import os
from google.cloud import storage
from google.api_core.exceptions import GoogleAPICallError

_GCS_CLIENT = None

def get_storage_client() -> storage.Client:
    """
    Initializes and returns a singleton Google Cloud Storage client.
    """
    global _GCS_CLIENT
    if _GCS_CLIENT is None:
        try:
            _GCS_CLIENT = storage.Client()
        except Exception as e:
            raise RuntimeError(f"Could not initialize Google Cloud Storage client. Ensure GOOGLE_APPLICATION_CREDENTIALS is set. Error: {e}")
    return _GCS_CLIENT

def get_bucket_name() -> str:
    """
    Retrieves the configured GCS bucket name from environment variables.
    """
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")
    return bucket_name

def get_bucket() -> storage.Bucket:
    """
    Helper function to get the configured GCS bucket object.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    try:
        return client.get_bucket(bucket_name)
    except GoogleAPICallError as e:
        raise RuntimeError(f"Could not get bucket '{bucket_name}'. Ensure the bucket exists and permissions are correct. Error: {e}")
