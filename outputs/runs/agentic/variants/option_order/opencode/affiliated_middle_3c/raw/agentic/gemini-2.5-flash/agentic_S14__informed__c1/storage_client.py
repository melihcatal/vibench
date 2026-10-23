import os
from google.cloud import storage


def get_storage_client():
    """
    Provides a Google Cloud Storage client.
    Authenticates using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    return storage.Client()
