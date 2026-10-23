import os
import boto3
from botocore.exceptions import ClientError
from storage_client import ManagedStorageClient


def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """Retrieve metadata/HEAD information for an object stored in Amazon S3.

    Args:
        bucket_name: S3 bucket name.
        object_key: Object key/path.

    Returns:
        Dictionary of metadata returned by S3 HEAD operation.
    """
    client = ManagedStorageClient.get_s3_client()
    try:
        response = client.head_object(Bucket=bucket_name, Key=object_key)
        return response
    except ClientError as e:
        raise RuntimeError(f"Metadata lookup failed: {e}")
