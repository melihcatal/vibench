class S3Object:
    def __init__(self, bucket_name, object_name, metadata):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.metadata = metadata
