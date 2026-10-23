import os
from typing import BinaryIO, Union

from boto3 import client
from botocore.exceptions import ClientError


class StorageClient:
    def __init__(self):
        self.client = client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def get_client(self):
        return self.client
