import boto3
from typing import List

from .storage_client import get_s3_client
from .storage_models import StorageObject, ListResult

s3 = get_s3_client()

def upload_object(bucket: str, key: str, body: bytes, content_type: str = 'application/octet-stream') -> None:
    """Upload a file or byte stream to AWS S3 (or any S3-compatible storage)."""
    s3.upload_object(bucket, key, body, content_type)

def presigned_download_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    """Generate a time‑limited presigned URL for downloading the object."""
    return s3.presigned_download_url(bucket, key, expires_in)

def get_object_metadata(bucket: str, key: str) -> StorageObject:
    """Head an object and return structured metadata."""
    head = s3.get_object_metadata(bucket, key)
    return StorageObject.from_s3_head(head)

def list_objects(prefix: str = '', delimiter: str = None, max_keys: int = None) -> ListResult:
    """List objects under a bucket prefix, returning normalized StorageObject entries."""
    objects = []
    prefixes = []
    paginator = s3.s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=s3.s3.meta.client.get_default_parameters().get('Bucket'), Prefix=prefix, Delimiter=delimiter, MaxKeys=max_keys):
        for item in page.get('Contents', []):
            objects.append(StorageObject.from_s3_head(item))
        for cp in page.get('CommonPrefixes', []):
            prefixes.append(cp.get('Prefix'))
    return ListResult(objects, prefixes)
