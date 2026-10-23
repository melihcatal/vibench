import os
from storage_client import get_s3_client
from storage_models import validate_bucket_and_key

def list_objects_under_prefix(bucket: str, prefix: str, max_keys: int = 1000):
    """List objects within a bucket that share the given prefix.

    bucket: S3 bucket name
    prefix: common path prefix (e.g., 'images/')
    max_keys: maximum number of items to return in a single request
    Returns a list of dicts, each containing at least 'Key' and 'Size'.
    """
    s3 = get_s3_client()
    validate_bucket_and_key(bucket, '')  # prefix is not a key so second arg dummy
    paginator = s3.get_paginator('list_objects_v2')
    kwargs = {'Bucket': bucket, 'Prefix': prefix, 'MaxKeys': max_keys}
    items = []
    for page in paginator.paginate(**kwargs):
        if 'Contents' in page:
            items.extend(page['Contents'])
    return items
