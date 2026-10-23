class S3Object:
    def __init__(self, bucket_name, object_key, metadata):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.metadata = metadata

    @classmethod
    def from_dict(cls, data):
        return cls(data['BucketName'], data['ObjectKey'], data['Metadata'])