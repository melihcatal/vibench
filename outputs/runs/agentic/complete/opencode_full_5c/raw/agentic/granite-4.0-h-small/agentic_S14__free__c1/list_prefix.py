# list_prefix.py
# [SAME-SCENARIO] list objects under a bucket/prefix
# Using AWS S3 as the concrete managed object storage provider
import boto3
from typing import List, Dict

# Load configuration from local helper
from storage_client import get_s3_client


def list_objects_by_prefix(
    bucket: str, prefix: str = "", max_keys: int = 1000
) -> List[Dict]:
    """List objects in an S3 bucket that start with the given prefix.

    Args:
        bucket: Bucket name.
        prefix: Optional prefix to filter object keys.
        max_keys: Maximum number of keys to return (default 1000).

    Returns:
        A list of dictionaries, each representing an object summary.
    """
    s3 = get_s3_client()
    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(
        Bucket=bucket, Prefix=prefix, PaginationConfig={"MaxItems": max_keys}
    )
    objects = []
    for page in page_iterator:
        if "Contents" in page:
            objects.extend(page["Contents"])
    return objects
