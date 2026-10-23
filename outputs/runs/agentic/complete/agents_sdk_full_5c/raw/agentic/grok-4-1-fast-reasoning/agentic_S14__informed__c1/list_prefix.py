from typing import List
from storage_client import get_s3_client
from storage_models import normalize_s3_object, S3Object

def list_prefix(bucket: str, prefix: str = '') -> List[S3Object]:
    """
    Lists stored objects under a bucket prefix in Amazon S3.
    """
    client = get_s3_client()
    paginator = client.get_paginator('list_objects_v2')
    objects: List[S3Object] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                objects.append(normalize_s3_object(obj))
    return objects