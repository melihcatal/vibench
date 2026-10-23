from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ObjectMetadataResult, isoformat_or_none, normalize_metadata


def get_object_metadata(bucket: str, key: str) -> ObjectMetadataResult:
    client = get_s3_client()
    response = client.head_object(Bucket=bucket, Key=key)
    return ObjectMetadataResult(
        bucket=bucket,
        key=key,
        etag=response.get("ETag"),
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        last_modified=isoformat_or_none(response.get("LastModified")),
        version_id=response.get("VersionId"),
        metadata=normalize_metadata(response.get("Metadata")),
    )
