import os
from google.cloud import storage


def get_storage_client() -> storage.Client:
    """Initializes and returns a Google Cloud Storage client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # with the path to your service account key file.
    # See https://cloud.google.com/docs/authentication/getting-started
    return storage.Client()
