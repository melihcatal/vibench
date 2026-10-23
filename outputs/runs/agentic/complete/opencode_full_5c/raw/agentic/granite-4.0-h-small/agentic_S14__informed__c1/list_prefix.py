# list_prefix.py
# Lists stored objects under a given bucket/prefix using S3

import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import ObjectMetadata


def list_objects_by_prefix(bucket: str, prefix: str, max_keys: int = 1000):
    """Return a list of ObjectMetadata for objects under the given prefix."""
    client = get_s3_client()
    paginator = client.get_paginator("list_objects_v2")
    list_iter = paginator.paginate(
        Bucket=bucket, Prefix=prefix, PaginationConfig={"MaxItems": max_keys}
    )
    results = []
    for page in list_iter:
        if "Contents" in page:
            for obj in page["Contents"]:
                results.append(ObjectMetadata(obj))
    return results


# Example usage:
# objects = list_objects_by_prefix("my-bucket", "images/")
# for o in objects:
#     print(o)
