import os
from google.cloud import storage


def get_storage_client():
    """
    Initializes and returns a Google Cloud Storage client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return storage.Client()
