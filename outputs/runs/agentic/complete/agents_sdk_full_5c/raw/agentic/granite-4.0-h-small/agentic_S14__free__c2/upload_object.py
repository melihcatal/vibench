import os
import boto3
from storage_client import get_s3_client

def upload_object(bucket_name, object_key, file_path_or_bytes, content_type='application/octet-stream'):
    """Upload a file or byte stream to AWS S3 (managed object storage).
    Uses boto3 SDK.
    """
    if isinstance(file_path_or_bytes, str):
        # Assume it's a file path
        with open(file_path_or_bytes, 'rb') as f:
            body = f.read()
    else:
        body = file_path_or_bytes
    s3 = get_s3_client()
    response = s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=body,
        ContentType=content_type
    )
    return response