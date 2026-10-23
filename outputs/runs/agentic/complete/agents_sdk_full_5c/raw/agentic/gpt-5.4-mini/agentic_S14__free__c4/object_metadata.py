from __future__ import annotations

from storage_client import get_bucket_name, get_s3_client
from storage_models import ObjectMetadata, normalize_datetime


def object_metadata(key: str) -> ObjectMetadata:
    s3 = get_s3_client()
    response = s3.head_object(Bucket=get_bucket_name(), Key=key)
    return ObjectMetadata(
        bucket=get_bucket_name(),
        key=key,
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        etag=response.get("ETag"),
        last_modified=normalize_datetime(response.get("LastModified")),
        metadata=response.get("Metadata") or {},
    )
