import boto3
from storage_client import get_s3_client

def list_objects_under_prefix(bucket_name: str, prefix: str, delimiter: str = ''):
    """List objects stored under a given bucket prefix.

    Uses AWS S3 ListObjectsV2 API.
    Returns a list of object keys matching the prefix.
    """
    client = get_s3_client()
    paginator = client.get_paginator('list_objects_v2')
    results = []
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix, Delimiter=delimiter):
        if 'Contents' in page:
            results.extend([obj['Key'] for obj in page['Contents']])
    return results