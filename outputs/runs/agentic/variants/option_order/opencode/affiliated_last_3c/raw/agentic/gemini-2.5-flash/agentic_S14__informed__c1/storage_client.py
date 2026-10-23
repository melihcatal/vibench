from google.cloud import storage
import os


def get_storage_client():
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return storage.Client()
