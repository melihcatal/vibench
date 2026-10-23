from google.cloud import storage

class StorageClient:
    def __init__(self):
        self.client = storage.Client()

    def get_client(self):
        return self.client
