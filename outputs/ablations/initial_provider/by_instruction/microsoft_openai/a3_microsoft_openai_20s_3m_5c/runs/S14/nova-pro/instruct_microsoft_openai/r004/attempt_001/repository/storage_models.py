from.storage_client import get_storage_client

class StorageRequest:
    def __init__(self, container_name, blob_name):
        self.container_name = container_name
        self.blob_name = blob_name

class StorageResponse:
    def __init__(self, status, data=None):
        self.status = status
        self.data = data