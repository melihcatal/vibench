from __future__ import annotations

from storage_client import require_bucket, s3_client
from storage_models import ObjectMetadata, isoformat_or_none, normalize_metadata


S3_PROVIDER = "Amazon S3"


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    client = s3_client()
    resolved_bucket = require_bucket(bucket)
    response = client.head_object(Bucket=resolved_bucket, Key=key)
    return ObjectMetadata(
        bucket=resolved_bucket,
        key=key,
        size=response.get("ContentLength"),
        etag=response.get("ETag"),
        content_type=response.get("ContentType"),
        last_modified=isoformat_or_none(response.get("LastModified")),
        metadata=normalize_metadata(response.get("Metadata")),
        storage_class=response.get("StorageClass"),
    )


def get_object_metadata_dict(bucket: str, key: str) -> dict:
    return get_object_metadata(bucket, key).to_dict()
