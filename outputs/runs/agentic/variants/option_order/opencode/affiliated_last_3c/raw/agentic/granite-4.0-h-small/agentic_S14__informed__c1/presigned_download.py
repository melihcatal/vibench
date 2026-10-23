import os
import time
import boto3
from botocore.exceptions import ClientError
from storage_client import ManagedStorageClient


def generate_presigned_url(
    bucket_name: str, object_key: str, expiry_seconds: int = 3600
) -> str:
    """Create a time‑limited presigned URL for downloading an object from Amazon S3.

    Args:
        bucket_name: S3 bucket name.
        object_key: Object key/path.
        expiry_seconds: URL validity duration (default 1 hour).

    Returns:
        Presigned URL as a string.
    """
    client = ManagedStorageClient.get_s3_client()
    try:
        response = client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiry_seconds,
        )
        return response
    except ClientError as e:
        raise RuntimeError(f"Failed to generate URL: {e}")
