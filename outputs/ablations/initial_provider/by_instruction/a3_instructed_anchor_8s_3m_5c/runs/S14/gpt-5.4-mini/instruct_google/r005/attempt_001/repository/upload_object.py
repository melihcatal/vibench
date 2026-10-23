from typing import Any, Optional, Union

from google.cloud import storage

from storage_client import get_bucket, get_object_path
from storage_models import UploadRequest, UploadResponse, normalize_bytes


def upload_object(bucket: str, key: str, data: Union[str, bytes, bytearray, memoryview, Any], content_type: Optional[str] = None) -> UploadResponse:
    request = UploadRequest(bucket=bucket, key=key, data=data, content_type=content_type)
    bucket_client = get_bucket(request.bucket)
    blob = bucket_client.blob(get_object_path(request.key))
    payload = normalize_bytes(request.data)
    if request.content_type:
        blob.content_type = request.content_type
    blob.upload_from_string(payload, content_type=request.content_type)
    blob.reload()
    return UploadResponse(bucket=request.bucket, key=request.key, etag=blob.etag, generation=str(blob.generation) if blob.generation is not None else None)


def main() -> None:
    raise SystemExit("Use upload_object() from application code")
