# SAME-SCENARIO object_metadata.py

# Uses Amazon S3 for managed object storage.
# Provider: Amazon S3
# SDK: boto3
# Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

import os
import boto3
from botocore.exceptions import ClientError


# Helper to get bucket name from env
def get_storage_config():
    bucket_name = os.getenv("S3_BUCKET_NAME")
    return bucket_name


def get_object_metadata(object_key: str, bucket_name: str = None):
    """Retrieves metadata for an object in S3.

    Args:
        object_key: Key of the object.
        bucket_name: Optional bucket; defaults to env var.

    Returns:
        dict of metadata.
    """
    if bucket_name is None:
        bucket_name = get_storage_config()
        if not bucket_name:
            raise RuntimeError("S3_BUCKET_NAME environment variable not set")

    s3 = boto3.client("s3")
    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        metadata = response.get("Metadata", {})
        print(f"Metadata for {object_key}: {metadata}")
        return metadata
    except ClientError as e:
        print(f"Error retrieving metadata for {object_key}: {e}")
        raise
