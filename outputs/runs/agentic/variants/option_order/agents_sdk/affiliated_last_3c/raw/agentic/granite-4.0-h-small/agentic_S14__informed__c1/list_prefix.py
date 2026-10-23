import os
from storage_client import get_s3_client
from storage_models import normalize_list_params

def list_objects_under_prefix(bucket, prefix, delimiter='/', max_keys=100):
    """Lists objects stored under a given prefix in an Amazon S3 bucket.
    Uses boto3 S3 client from storage_client.py.
    Returns a list of object keys matching the prefix.
    """
    params = normalize_list_params(bucket, prefix, delimiter, max_keys)
    s3 = get_s3_client()
    paginator = s3.get_paginator('list_objects_v2')
    results = []
    for page in paginator.paginate(**params):
        if 'Contents' in page:
            results.extend(page['Contents'])
    print(f'Listed {len(results)} objects under prefix {prefix} in bucket {bucket}.')
    return results
