import os

from google.cloud import storage


def get_storage_client(config=None):
    config = config or {}
    return storage.Client(project=config["project_id"])