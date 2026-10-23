import os
from storage_client import get_managed_storage_client


def list_objects_by_prefix(bucket_name, prefix="", max_keys=1000):
    """List objects under a bucket prefix using IBM Cloud Object Storage.

    Returns a list of object keys matching the prefix.
    """
    cos = get_managed_storage_client()
    paginator = cos.get_paginator("list_objects_v2")
    results = []
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys):
        if "Contents" in page:
            results.extend([obj["Key"] for obj in page["Contents"]])
    return results
