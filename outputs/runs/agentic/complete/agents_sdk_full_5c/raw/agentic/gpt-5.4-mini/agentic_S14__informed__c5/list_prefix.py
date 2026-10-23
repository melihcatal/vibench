from __future__ import annotations

from google.cloud import storage

from storage_client import get_bucket
from storage_models import ListedObject, ObjectListResult, PrefixListRequest, normalize_datetime


def list_objects_with_prefix(bucket: str, prefix: str = "", max_results: int | None = None) -> ObjectListResult:
    request = PrefixListRequest(bucket=bucket, prefix=prefix, max_results=max_results)
    blobs = get_bucket(request.bucket).list_blobs(prefix=request.prefix, max_results=request.max_results)
    objects = [
        ListedObject(
            key=blob.name,
            size=blob.size,
            last_modified=normalize_datetime(getattr(blob, "updated", None)),
            etag=getattr(blob, "etag", None),
        )
        for blob in blobs
    ]
    return ObjectListResult(bucket=request.bucket, prefix=request.prefix, objects=objects)
