from __future__ import annotations

from storage_client import get_s3_client
from storage_models import (
    ObjectMetadataResult,
    normalize_datetime,
    normalize_metadata_map,
)


def get_object_metadata(bucket: str, key: str) -> ObjectMetadataResult:
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket, Key=key)
    return ObjectMetadataResult(
        bucket=bucket,
        key=key,
        size=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        etag=response.get("ETag"),
        last_modified=normalize_datetime(response.get("LastModified")),
        metadata=normalize_metadata_map(response.get("Metadata")),
        version_id=response.get("VersionId"),
    )
