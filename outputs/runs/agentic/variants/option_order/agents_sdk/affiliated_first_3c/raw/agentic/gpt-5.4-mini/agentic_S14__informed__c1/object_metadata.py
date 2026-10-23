from __future__ import annotations

from google.cloud import storage

from storage_client import get_bucket
from storage_models import ObjectMetadata, normalize_metadata


def read_object_metadata(bucket_name: str, object_name: str) -> ObjectMetadata:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.reload()
    return ObjectMetadata(
        bucket=bucket_name,
        name=object_name,
        size=blob.size,
        content_type=blob.content_type,
        md5_hash=blob.md5_hash,
        etag=getattr(blob, "etag", None),
        metadata=normalize_metadata(blob.metadata),
        updated=str(blob.updated) if blob.updated else None,
    )
