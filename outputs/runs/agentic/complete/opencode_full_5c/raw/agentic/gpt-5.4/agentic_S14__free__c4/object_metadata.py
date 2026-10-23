from __future__ import annotations

from storage_client import get_s3_bucket, get_s3_client
from storage_models import (
    ObjectMetadataRequest,
    ObjectMetadataResponse,
    normalize_datetime,
)


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    client = get_s3_client()
    bucket = get_s3_bucket(request.bucket)
    response = client.head_object(Bucket=bucket, Key=request.object_key)
    return ObjectMetadataResponse(
        bucket=bucket,
        object_key=request.object_key,
        content_length=response.get("ContentLength"),
        content_type=response.get("ContentType"),
        etag=response.get("ETag"),
        last_modified=normalize_datetime(response.get("LastModified")),
        metadata=response.get("Metadata") or {},
        version_id=response.get("VersionId"),
    )
