import os
import boto3
from storage_client import get_s3_client

def upload_object(bucket_name: str, object_key: str, file_path: str = None, data: bytes = None):
    """Upload a file or byte stream to a managed object storage bucket.

    Uses AWS S3 as the concrete managed object storage provider.
    """
    client = get_s3_client()
    if file_path:
        client.upload_file(file_path, bucket_name, object_key)
    elif data:
        client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
    else:
        raise ValueError("Must provide either file_path or data")