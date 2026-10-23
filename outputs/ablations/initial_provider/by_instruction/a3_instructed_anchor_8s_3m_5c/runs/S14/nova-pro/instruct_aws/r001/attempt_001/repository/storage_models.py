class S3Object:
    def __init__(self, bucket, key, metadata):
        self.bucket = bucket
        self.key = key
        self.metadata = metadata

    @staticmethod
    def from_response(response):
        return S3Object(
            bucket=response['Bucket'],
            key=response['Key'],
            metadata=response.get('Metadata', {})
        )