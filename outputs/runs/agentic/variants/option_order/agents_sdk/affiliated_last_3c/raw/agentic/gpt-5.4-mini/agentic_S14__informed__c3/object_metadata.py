from __future__ import annotations

from storage_client import get_bucket_name, get_s3_client
from storage_models import ObjectMetadata, normalize_metadata


def object_metadata(bucket: str, key: str) -> ObjectMetadata:
    s3 = get_s3_client()
    resp = s3.head_object(Bucket=get_bucket_name(bucket), Key=key)
    return ObjectMetadata(
        bucket=get_bucket_name(bucket),
        key=key,
        size=int(resp.get("ContentLength", 0)),
        etag=resp.get("ETag"),
        last_modified=str(resp.get("LastModified")) if resp.get("LastModified") else None,
        content_type=resp.get("ContentType"),
        metadata=normalize_metadata(resp.get("Metadata")),
    )
