# upload_object.py
import os
from storage_client import ManagedStorageClient
from storage_models import UploadResponse

def upload_object(bucket: str, object_key: str, file_path: str | bytes, content_type: str = "application/octet-stream") -> UploadResponse:
    """Upload a file or byte stream to managed object storage using a concrete provider.

    Args:
        bucket: The bucket/container name.
        object_key: The object's key/path within the bucket.
        file_path: Local file path or bytes to upload.
        content_type: MIME type of the object.

    Returns:
        UploadResponse with the result of the upload operation.
    """
    client = ManagedStorageClient()
    # Ensure we have a bytes-like object for upload
    if isinstance(file_path, str):
        with open(file_path, "rb") as f:
            body = f.read()
    else:
        body = file_path
    result = client.upload(bucket, object_key, body, content_type=content_type)
    return UploadResponse(status=result['status'], bucket=result['bucket'], key=result['key'])
