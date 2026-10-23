class S3Object:
    def __init__(self, bucket_name, key):
        self.bucket_name = bucket_name
        self.key = key

    def __repr__(self):
        return f'S3Object(bucket_name={self.bucket_name}, key={self.key})'