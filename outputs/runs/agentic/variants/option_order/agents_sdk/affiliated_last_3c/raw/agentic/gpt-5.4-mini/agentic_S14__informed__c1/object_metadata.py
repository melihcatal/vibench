from __future__ import annotations

from storage_client import resolve_key, s3_client
from storage_models import ObjectMetadata, normalize_s3_metadata


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    client = s3_client()
    object_key = resolve_key(key)
    response = client.head_object(Bucket=bucket, Key=object_key)
    return normalize_s3_metadata(response, bucket=bucket, key=object_key)
