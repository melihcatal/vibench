# object_metadata.py
# [SAME-SCENARIO] retrieve object metadata/HEAD information
# Using AWS S3 as the concrete managed object storage provider
import boto3
from typing import Dict

# Load configuration from local helper
from storage_client import get_s3_client, get_bucket_name


def get_object_metadata(bucket: str, key: str) -> Dict:
    """Get metadata (HEAD) for an object stored in S3.

    Returns a dict containing metadata fields returned by S3.
    """
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket, Key=key)
    return response
