from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ObjectMetadataResult, coerce_metadata, normalize_timestamp


def get_object_metadata(bucket: str, key: str) -> ObjectMetadataResult:
    s3 = get_s3_client("s3")
    response = s3.head_object(Bucket=bucket, Key=key)
    return ObjectMetadataResult(
        bucket=bucket,
        key=key,
        size=response.get("ContentLength"),
        etag=response.get("ETag"),
        content_type=response.get("ContentType"),
        last_modified=normalize_timestamp(response.get("LastModified")),
        metadata=coerce_metadata(response.get("Metadata")),
        version_id=response.get("VersionId"),
    )
