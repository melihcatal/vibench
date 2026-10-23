import os
from google.cloud import storage

def get_gcs_client():
    """Return a configured GCS client using env var GOOGLE_APPLICATION_CREDENTIALS."""
    return storage.Client()
