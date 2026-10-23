from google.cloud import storage
import os


class StorageClient:
    def __init__(self):
        self._client = storage.Client()

    def get_client(self):
        return self._client
