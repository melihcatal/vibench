# SAME-SCENARIO list_prefix.py

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


def list_objects_under_prefix(prefix: str, bucket_name: str = None):
    """Lists objects in S3 under a given prefix.

    Args:
        prefix: Prefix string; acts like a folder path.
        bucket_name: Optional bucket; defaults to env var.

    Returns:
        List of object keys under the prefix.
    """
    if bucket_name is None:
        bucket_name = get_storage_config()
        if not bucket_name:
            raise RuntimeError("S3_BUCKET_NAME environment variable not set")

    s3 = boto3.client("s3")
    try:
        paginator = s3.get_paginator("list_objects_v2")
        keys = []
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
            if "Contents" in page:
                keys.extend([obj["Key"] for obj in page["Contents"]])
        print(f"Objects under prefix {prefix}: {keys}")
        return keys
    except ClientError as e:
        print(f"Error listing objects under prefix {prefix}: {e}")
        raise
