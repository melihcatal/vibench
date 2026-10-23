import os
from storage_client import get_s3_client

def list_objects_by_prefix(bucket_name, prefix, max_keys=1000):
    """List objects under a given prefix in Amazon S3.
    Returns a list of object keys matching the prefix.
    """
    s3 = get_s3_client()
    paginator = s3.get_paginator('list_objects_v2')
    results = []
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix, PaginationConfig={'MaxKeys': max_keys}):
        if 'Contents' in page:
            results.extend([obj['Key'] for obj in page['Contents']])
    return results
