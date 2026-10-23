import boto3
from typing import List

from .storage_client import get_s3_client
from .storage_models import StorageObject, ListResult

s3 = get_s3_client()

def list_prefix(bucket: str, prefix: str = '', delimiter: str = None, max_keys: int = None) -> ListResult:
    """List objects that start with the given prefix (folder emulation)."""
    objects = []
    prefixes = []
    paginator = s3.s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter=delimiter, MaxKeys=max_keys):
        for item in page.get('Contents', []):
            objects.append(StorageObject.from_s3_head(item))
        for cp in page.get('CommonPrefixes', []):
            prefixes.append(cp.get('Prefix'))
    return ListResult(objects, prefixes)
