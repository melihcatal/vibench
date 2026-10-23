# [SAME-SCENARIO] list_prefix.py

import boto3

from storage_client import get_managed_storage_client


def list_objects_by_prefix(
    bucket_name: str, prefix: str = "", max_keys: int = 1000
) -> list:
    """List objects stored under a given bucket prefix.

    Uses AWS S3‑compatible managed object storage (e.g., Amazon S3, MinIO).
    Returns a list of dicts with object keys and metadata.
    """
    client = get_managed_storage_client()
    paginator = client.get_paginator("list_objects_v2")
    response_iterator = paginator.paginate(
        Bucket=bucket_name,
        Prefix=prefix,
        PaginationConfig={"MaxItems": max_keys, "PageSize": 1000},
    )
    objects = []
    for page in response_iterator:
        if "Contents" in page:
            objects.extend(page["Contents"])
    return objects
