from typing import Any

from google.cloud import storage

from storage_client import get_bucket
from storage_models import StorageObjectRequest, StorageObjectResponse, normalize_object_name


def upload_object(bucket: str, object_name: str, data: Any, content_type: str = None, metadata=None) -> StorageObjectResponse:
    request = StorageObjectRequest(bucket=bucket, object_name=normalize_object_name(object_name), data=data, content_type=content_type, metadata=metadata or {})
    blob = get_bucket(request.bucket).blob(request.object_name)
    if request.metadata:
        blob.metadata = request.metadata
    blob.upload_from_string(request.data if isinstance(request.data, (str, bytes)) else request.data.read(), content_type=request.content_type)
    blob.reload()
    return StorageObjectResponse(bucket=request.bucket, object_name=request.object_name, uri=f"gs://{request.bucket}/{request.object_name}", etag=blob.etag, size=blob.size, content_type=blob.content_type, metadata=dict(blob.metadata or {}))
