# SAME-SCENARIO presigned_download.py

# Uses Amazon S3 for managed object storage.
# Provider: Amazon S3
# SDK: boto3
# Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta


# Helper to get bucket name from env
def get_storage_config():
    bucket_name = os.getenv("S3_BUCKET_NAME")
    return bucket_name


def create_presigned_download_url(
    object_key: str, bucket_name: str = None, expires_hours: int = 1
):
    """Generates a time-limited URL for downloading an object.

    Args:
        object_key: Key of the object in S3.
        bucket_name: Optional bucket; defaults to env var.
        expires_hours: How many hours the URL remains valid.

    Returns:
        String URL.
    """
    if bucket_name is None:
        bucket_name = get_storage_config()
        if not bucket_name:
            raise RuntimeError("S3_BUCKET_NAME environment variable not set")

    s3 = boto3.client("s3")
    try:
        response = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expires_hours * 3600,
        )
        print(f"Presigned download URL for {object_key}: {response}")
        return response
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        raise
