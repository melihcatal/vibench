import os
import boto3
from .storage_client import StorageClient
from .storage_models import ObjectMetadata


class ObjectMetadataReader:
    """Retrieve HEAD/object metadata from Managed Object Storage (S3)."""

    @classmethod
    def head(cls, bucket_name: str, key: str) -> ObjectMetadata:
        response = StorageClient.s3.head_object(
            Bucket=bucket_name,
            Key=key,
        )
        return ObjectMetadata.from_s3(response)
