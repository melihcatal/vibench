from __future__ import annotations

from typing import BinaryIO, Optional, Union

from google.cloud import storage

from storage_client import get_bucket
from storage_models import UploadRequest, normalize_metadata


def upload_object(
    bucket_name: str,
    object_name: str,
    data: Union[bytes, BinaryIO],
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> str:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    request = UploadRequest(bucket=bucket_name, name=object_name, content_type=content_type, metadata=metadata)
    if isinstance(data, (bytes, bytearray)):
        blob.metadata = normalize_metadata(request.metadata)
        blob.upload_from_string(data, content_type=request.content_type)
    else:
        blob.metadata = normalize_metadata(request.metadata)
        blob.upload_from_file(data, content_type=request.content_type)
    return f"gs://{bucket_name}/{object_name}"
