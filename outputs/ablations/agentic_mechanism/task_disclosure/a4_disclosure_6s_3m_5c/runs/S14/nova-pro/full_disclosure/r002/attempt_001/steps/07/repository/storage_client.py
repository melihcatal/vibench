import boto3

class StorageClient:
    def __init__(self, region_name, access_key, secret_key):
        self.s3_client = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def get_client(self):
        return self.s3_client