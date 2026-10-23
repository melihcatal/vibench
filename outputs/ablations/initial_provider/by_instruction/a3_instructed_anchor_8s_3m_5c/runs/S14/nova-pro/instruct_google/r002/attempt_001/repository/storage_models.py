class StorageRequest:
    def __init__(self, bucket_name, blob_name, source_file_name=None, destination_blob_name=None, expiration=None):
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        self.source_file_name = source_file_name
        self.destination_blob_name = destination_blob_name
        self.expiration = expiration

class StorageResponse:
    def __init__(self, url=None, metadata=None):
        self.url = url
        self.metadata = metadata