from storage_client import get_s3_client
from storage_models import normalize_object_list, ObjectInfo
from typing import List

def list_objects_prefix(bucket: str, prefix: str = '') -> List[ObjectInfo]:
    """
    Lists S3 objects under a bucket prefix.
    """
    s3 = get_s3_client()
    paginator = s3.get_paginator('list_objects_v2')
    objects = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' in page:
            objects.extend(normalize_object_list(page['Contents']))
    return objects