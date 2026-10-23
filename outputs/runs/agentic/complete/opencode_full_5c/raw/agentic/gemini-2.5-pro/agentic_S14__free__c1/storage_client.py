from google.cloud import storage
import os


def get_storage_client():
    """Initializes and returns a Google Cloud Storage client."""
    # This will automatically use the credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS) or the default service account.
    return storage.Client()
