class S3Object:
    def __init__(self, bucket_name, object_key):
        self.bucket_name = bucket_name
        self.object_key = object_key

    def __repr__(self):
        return f'S3Object(bucket_name={self.bucket_name}, object_key={self.object_key})'