import os
from typing import Dict, Any

def validate_bucket_and_key(bucket: str, key: str) -> None:
    """Raise ValueError if bucket or key string appear malformed.
    Simple sanity checks suitable for local helpers.
    """
    if not bucket or not isinstance(bucket, str):
        raise ValueError('Invalid bucket name')
    if not key or not isinstance(key, str):
        raise ValueError('Invalid object key')

def normalize_object_info(info: Dict[str, Any]) -> Dict[str, Any]:
    """Extract common fields from raw S3 or OSS response into a normalized model.
    Returns a dict with keys: 'key', 'size', 'last_modified', 'etag', 'content_type'.
    """
    return {
        'key': info.get('Key'),
        'size': info.get('Size'),
        'last_modified': info.get('LastModified'),
        'etag': info.get('ETag'),
        'content_type': info.get('ContentType')  # S3 uses ContentType
    }
