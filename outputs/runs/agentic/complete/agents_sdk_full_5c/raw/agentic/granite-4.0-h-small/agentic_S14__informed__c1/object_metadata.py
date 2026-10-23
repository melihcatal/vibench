import boto3
from typing import Optional

from .storage_client import get_s3_client
from .storage_models import StorageObject

s3 = get_s3_client()

def object_metadata(bucket: str, key: str) -> Optional[StorageObject]:
    """Retrieve HEAD metadata for an object and return a normalized StorageObject."""
    try:
        head = s3.s3.head_object(Bucket=bucket, Key=key)
        return StorageObject.from_s3_head(head)
    except Exception as e:
        raise RuntimeError(f'Failed to fetch metadata: {e}')
