from __future__ import annotations

from typing import Any, Optional

from google.cloud import storage

from storage_client import get_bucket
from storage_models import UploadRequest, ObjectMetadata, normalize_datetime


def upload_object(bucket: str, key: str, body: Any, content_type: Optional[str] = None, metadata: Optional[dict[str, str]] = None) -> ObjectMetadata:
    request = UploadRequest(bucket=bucket, key=key, body=body, content_type=content_type, metadata=metadata or {})
    bucket_ref = get_bucket(request.bucket)
    blob = bucket_ref.blob(request.key)
    if request.metadata:
        blob.metadata = dict(request.metadata)
    if request.content_type:
        blob.content_type = request.content_type
    blob.upload_from_file(request.body, rewind=True) if hasattr(request.body, "read") else blob.upload_from_string(request.body)
    blob.reload()
    return ObjectMetadata(
        bucket=request.bucket,
        key=request.key,
        size=blob.size,
        content_type=blob.content_type,
        etag=getattr(blob, "etag", None),
        last_modified=normalize_datetime(getattr(blob, "updated", None)),
        metadata=dict(blob.metadata or {}),
    )
