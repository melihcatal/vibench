import os
import boto3
from botocore.exceptions import ClientError


def upload_object(
    bucket_name, key, file_path_or_bytes, content_type="application/octet-stream"
):
    """Upload a file or byte stream to Amazon S3.

    Uses AWS SDK (boto3) which identifies the provider as Amazon S3.
    """
    # Determine if file_path_or_bytes is a path (string) or bytes
    if isinstance(file_path_or_bytes, str):
        # Assume local file path
        with open(file_path_or_bytes, "rb") as f:
            body = f.read()
    elif isinstance(file_path_or_bytes, bytes):
        body = file_path_or_bytes
    else:
        raise ValueError("file_path_or_bytes must be a path string or bytes")

    s3 = boto3.client("s3")
    try:
        s3.put_object(Bucket=bucket_name, Key=key, Body=body, ContentType=content_type)
        print(f"Uploaded {key} to {bucket_name}")
    except ClientError as e:
        print("Error uploading object:", e)
