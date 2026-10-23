from google.cloud import storage
import os

def get_storage_client():
    """Returns a Google Cloud Storage client instance."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or running in a Google Cloud environment.
    return storage.Client()
