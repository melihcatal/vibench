from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ObjectMetadataResponse, normalize_s3_head


def get_object_metadata(bucket: str, key: str) -> ObjectMetadataResponse:
    s3 = get_s3_client()
    payload = s3.head_object(Bucket=bucket, Key=key)
    return normalize_s3_head(bucket, key, payload)
