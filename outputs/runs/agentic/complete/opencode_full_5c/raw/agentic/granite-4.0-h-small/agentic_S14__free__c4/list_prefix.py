import boto3
from storage_client import get_managed_storage_client


def list_objects_by_prefix(bucket_name: str, prefix: str, max_keys: int = 1000):
    """List stored objects under a bucket or container prefix.

    Uses AWS S3-compatible managed object storage.
    """
    client = get_managed_storage_client()
    paginator = client.get_paginator("list_objects_v2")
    results = []
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys):
        if "Contents" in page:
            results.extend(page["Contents"])
    return results
