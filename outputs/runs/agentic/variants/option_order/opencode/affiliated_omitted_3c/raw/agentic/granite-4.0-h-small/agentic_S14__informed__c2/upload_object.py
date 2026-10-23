# SAME-SCENARIO upload_object.py

# Uses Amazon S3 for managed object storage.
# Provider: Amazon S3
# SDK: boto3
# Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

import os
import boto3
from botocore.exceptions import ClientError


# Helper to get bucket name and object key from environment
def get_storage_config():
    bucket_name = os.getenv("S3_BUCKET_NAME")
    return bucket_name


def upload_object(file_path: str, object_key: str, bucket_name: str = None):
    """Uploads a local file or byte stream to S3.

    Args:
        file_path: Path to a local file or a path that contains the data as string.
        object_key: Target key name in S3.
        bucket_name: Optional bucket name; if omitted, taken from env.
    """
    if bucket_name is None:
        bucket_name = get_storage_config()
        if not bucket_name:
            raise RuntimeError("S3_BUCKET_NAME environment variable not set")

    s3 = boto3.client("s3")

    try:
        # Determine if file_path points to a real file or a byte string
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                s3.upload_file(file_path, bucket_name, object_key)
            print(f"Uploaded file {file_path} to s3://{bucket_name}/{object_key}")
        else:
            # Assume file_path is a byte string
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_path)
            print(f"Uploaded byte stream to s3://{bucket_name}/{object_key}")
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        raise
