class S3Object:
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

    def to_dict(self):
        return {'bucket': self.bucket, 'key': self.key}