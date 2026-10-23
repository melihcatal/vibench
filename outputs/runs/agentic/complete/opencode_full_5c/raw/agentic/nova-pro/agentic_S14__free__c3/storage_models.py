class S3Object:
    def __init__(self, bucket_name, object_key, metadata):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.metadata = metadata


class PresignedUrl:
    def __init__(self, url, expiration):
        self.url = url
        self.expiration = expiration
