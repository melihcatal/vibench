class S3Object:
    def __init__(self, bucket_name, object_key):
        self.bucket_name = bucket_name
        self.object_key = object_key