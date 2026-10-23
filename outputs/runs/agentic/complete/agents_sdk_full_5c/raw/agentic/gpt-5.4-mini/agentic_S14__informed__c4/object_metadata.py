from __future__ import annotations

from storage_client import coerce_bucket, get_s3_client
from storage_models import HeadObjectResult


def object_metadata(bucket: str, key: str) -> HeadObjectResult:
    client = get_s3_client()
    bucket = coerce_bucket(bucket)
    response = client.head_object(Bucket=bucket, Key=key)
    return HeadObjectResult(
        bucket=bucket,
        key=key,
        etag=response.get("ETag"),
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        last_modified=response.get("LastModified"),
        metadata=response.get("Metadata", {}),
    )
