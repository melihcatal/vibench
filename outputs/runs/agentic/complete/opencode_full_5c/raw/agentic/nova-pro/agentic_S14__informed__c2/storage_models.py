class StorageObject:
    def __init__(self, bucket_name, object_name):
        self.bucket_name = bucket_name
        self.object_name = object_name

    def __repr__(self):
        return f"StorageObject(bucket_name={self.bucket_name}, object_name={self.object_name})"
