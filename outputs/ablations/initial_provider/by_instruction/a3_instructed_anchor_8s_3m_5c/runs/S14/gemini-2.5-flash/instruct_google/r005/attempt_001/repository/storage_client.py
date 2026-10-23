from google.cloud import storage
import os

def get_storage_client():
    """Initializes and returns a Google Cloud Storage client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or rely on Google Cloud's default credential discovery.
    return storage.Client()
