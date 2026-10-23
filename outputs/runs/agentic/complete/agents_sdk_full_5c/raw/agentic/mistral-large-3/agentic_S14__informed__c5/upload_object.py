from google.cloud import storage
import os
from typing import Union, BinaryIO
from storage_models import UploadRequest, UploadResponse
from storage_client import get_storage_client

def upload_object(request: UploadRequest) -> UploadResponse:
    """Upload a file or byte stream to Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_key)

    if isinstance(request.content, (bytes, str)):
        blob.upload_from_string(request.content, content_type=request.content_type)
    elif isinstance(request.content, BinaryIO):
        blob.upload_from_file(request.content, content_type=request.content_type)
    else:
        raise ValueError("Content must be bytes, str, or BinaryIO")

    return UploadResponse(
        bucket_name=request.bucket_name,
        object_key=request.object_key,
        public_url=blob.public_url,
        size=blob.size,
        etag=blob.etag
    )