import os
import boto3
from .storage_client import StorageClient
from .storage_models import ObjectMetadata


class UploadObject:
    """Upload a local file or byte stream to Managed Object Storage using Amazon S3."""

    @classmethod
    def upload(cls, bucket_name: str, key: str, source: str, **kwargs):
        """source can be a file path or a bytes/bytearray object."""
        if isinstance(source, (bytes, bytearray)):
            body = source
        else:
            # treat as a local file path
            with open(source, "rb") as f:
                body = f.read()
        # Use the storage client to perform the upload
        response = StorageClient.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=body,
            **kwargs,
        )
        # Return a simple success indicator
        return {
            "status": "uploaded",
            "bucket": bucket_name,
            "key": key,
            "response": response,
        }
