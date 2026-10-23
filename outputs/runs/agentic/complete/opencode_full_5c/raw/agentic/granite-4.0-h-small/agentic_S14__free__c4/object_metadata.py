import boto3
from storage_client import get_managed_storage_client


def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """Retrieve object metadata / HEAD information from managed object storage.

    Uses AWS S3-compatible managed object storage.
    """
    client = get_managed_storage_client()
    response = client.head_object(Bucket=bucket_name, Key=object_key)
    return response
