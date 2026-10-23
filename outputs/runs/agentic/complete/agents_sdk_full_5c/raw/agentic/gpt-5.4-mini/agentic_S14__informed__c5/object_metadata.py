from __future__ import annotations

from storage_client import get_bucket
from storage_models import ObjectMetadata, normalize_datetime


def read_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    blob = get_bucket(bucket).blob(key)
    blob.reload()
    return ObjectMetadata(
        bucket=bucket,
        key=key,
        size=blob.size,
        content_type=blob.content_type,
        etag=getattr(blob, "etag", None),
        last_modified=normalize_datetime(getattr(blob, "updated", None)),
        metadata=dict(blob.metadata or {}),
    )
