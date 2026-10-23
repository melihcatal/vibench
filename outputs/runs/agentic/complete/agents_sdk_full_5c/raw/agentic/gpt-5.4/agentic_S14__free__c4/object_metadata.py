from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ObjectMetadata, normalize_s3_metadata


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket, Key=key)
    return normalize_s3_metadata(bucket=bucket, key=key, response=response)
