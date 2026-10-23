import os
from typing import Optional

from boto3 import client
from botocore.client import Config


class StorageClient:
    """
    A helper class for AWS S3 client configuration and utilities.
    """

    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.client = client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=self.region_name,
            config=Config(signature_version="s3v4"),
        )

    def get_client(self):
        """Returns the configured S3 client."""
        return self.client
