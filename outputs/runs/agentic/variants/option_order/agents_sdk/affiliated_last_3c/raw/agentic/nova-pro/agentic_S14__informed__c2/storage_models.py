class StorageObject:
    def __init__(self, bucket_name, object_name, metadata=None):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.metadata = metadata