class StorageRequest:
    def __init__(self, bucket_name, blob_name):
        self.bucket_name = bucket_name
        self.blob_name = blob_name

class StorageResponse:
    def __init__(self, status, data):
        self.status = status
        self.data = data