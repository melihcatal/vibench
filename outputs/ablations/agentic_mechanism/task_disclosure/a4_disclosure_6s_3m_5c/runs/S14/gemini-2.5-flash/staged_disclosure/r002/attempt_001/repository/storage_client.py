import boto3

class StorageClient:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def upload_file(self, file_name, bucket_name, object_name=None):
        if object_name is None:
            object_name = file_name
        self.s3_client.upload_file(file_name, bucket_name, object_name)
