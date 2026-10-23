import os
from google.cloud import storage

def get_storage_client() -> storage.Client:
    """
    Initializes and returns a Google Cloud Storage client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    return storage.Client()