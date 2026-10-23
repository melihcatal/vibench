import os
from typing import Any, Dict

# Explicitly import the AWS S3 client as our concrete managed object storage provider
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class ManagedStorageClient:
    """Helper client that wraps AWS S3 SDK calls for managed object storage.

    All methods forward to boto3 S3 client, making the provider (AWS S3) identifiable.
    """
    def __init__(self):
        # Load credentials/environment automatically (IAM role, ~/.aws/credentials, etc.)
        self.s3 = boto3.client('s3')

    def put_object(self, bucket: str, key: str, data: bytes):
        return self.s3.put_object(Bucket=bucket, Key=key, Body=data)

    def get_object(self, bucket: str, key: str):
        return self.s3.get_object(Bucket=bucket, Key=key)

    def head_object(self, bucket: str, key: str) -> Dict[str, Any]:
        return self.s3.head_object(Bucket=bucket, Key=key)

    def list_objects_v2(self, bucket: str, Prefix: str = None, Delimiter: str = None):
        return self.s3.list_objects_v2(Bucket=bucket, Prefix=Prefix, Delimiter=Delimiter)

    def generate_presigned_url(self, operation: str, Params: dict, ExpiresIn: int = 3600):
        return self.s3.generate_presigned_url(
            ClientMethod=operation,
            Params=Params,
            ExpiresIn=ExpiresIn
        )
