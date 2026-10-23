from boto3 import client

class StorageClient:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.client = client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def get_client(self):
        return self.client