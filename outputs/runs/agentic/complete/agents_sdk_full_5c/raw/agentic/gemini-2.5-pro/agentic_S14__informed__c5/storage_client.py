import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

_storage_client = None

def get_storage_client() -> storage.Client:
    """Initializes and returns a singleton Google Cloud Storage client."""
    global _storage_client
    if _storage_client is None:
        # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
        _storage_client = storage.Client()
    return _storage_client

def get_bucket_name() -> str:
    """Returns the configured GCS bucket name from environment variables."""
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")
    return bucket_name
