import os
import boto3
from botocore.exceptions import ClientError
from storage_client import ManagedStorageClient


def upload_object(
    bucket_name: str, object_key: str, file_path: str = None, data: bytes = None
) -> dict:
    """Upload a file or byte stream to Amazon S3 (managed object storage).

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Destination key (path) within the bucket.
        file_path: Local file path to upload. Either file_path or data must be provided.
        data: Bytes to upload directly.

    Returns:
        Dict response from S3 containing VersionId, ETag, etc.
    """
    client = ManagedStorageClient.get_s3_client()
    try:
        if file_path:
            client.upload_file(file_path, bucket_name, object_key)
        elif data:
            client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
        else:
            raise ValueError("Either file_path or data must be provided.")
        return {"status": "uploaded", "object_key": object_key}
    except ClientError as e:
        return {"error": str(e)}
