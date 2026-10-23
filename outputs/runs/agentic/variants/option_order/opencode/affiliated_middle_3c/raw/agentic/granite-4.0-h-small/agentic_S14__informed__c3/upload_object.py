import os
import boto3


def upload_object(bucket_name, object_key, file_path_or_bytes):
    """Upload a file or byte stream to Amazon S3.

    Uses the AWS SDK (boto3) – provider is identified by boto3 import
    and environment variables AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY.
    """
    s3 = boto3.client("s3")
    if isinstance(file_path_or_bytes, str):
        # Assume it is a local file path
        s3.upload_file(file_path_or_bytes, bucket_name, object_key)
    else:
        # Treat as bytes and use put_object
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_path_or_bytes)

    print(f"Uploaded {object_key} to bucket {bucket_name}")
