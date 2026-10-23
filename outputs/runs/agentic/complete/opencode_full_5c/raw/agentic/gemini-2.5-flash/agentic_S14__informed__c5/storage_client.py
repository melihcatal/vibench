import os
from google.cloud import storage


def get_gcs_client():
    return storage.Client()
