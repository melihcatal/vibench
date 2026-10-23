import os
from google.cloud import storage


def get_storage_client():
    """
    Initializes and returns a Google Cloud Storage client.

    Assumes that the environment variable GOOGLE_APPLICATION_CREDENTIALS
    is set to the path of a valid service account JSON file.
    """
    return storage.Client()
