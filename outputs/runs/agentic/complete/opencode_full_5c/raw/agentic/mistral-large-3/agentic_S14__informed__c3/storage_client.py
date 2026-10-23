import os
from typing import Optional

import boto3
from botocore.client import Config


class StorageClient:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
        )

    def get_client(self):
        return self.s3_client

    def get_bucket_region(self, bucket_name: str) -> Optional[str]:
        try:
            response = self.s3_client.get_bucket_location(Bucket=bucket_name)
            return response.get("LocationConstraint") or "us-east-1"
        except Exception as e:
            raise Exception(f"Failed to get bucket region: {e}")
