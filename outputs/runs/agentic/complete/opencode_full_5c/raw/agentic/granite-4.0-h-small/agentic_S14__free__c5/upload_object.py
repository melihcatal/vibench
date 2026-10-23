# upload_object.py
# [SAME-SCENARIO] Uploads a file or byte stream to managed object storage

import json
import os
from google.cloud import storage
from storage_client import ManagedStorageClient
from storage_models import UploadResponse

"
# Sample call (for documentation only, remove in production):
# upload_object(bucket_name='my-bucket', source_path='local/file.txt', destination_blob_name='remote/file.txt)"
"

def upload_object(bucket_name: str, source_path: str | bytes, destination_blob_name: str) -> UploadResponse:
    """Upload a local file or byte stream to the specified bucket using the managed storage client.

    Args:
        bucket_name (str): Name of the bucket/container.
        source_path (str | bytes): Path to a local file or raw bytes to upload.
        destination_blob_name (str): Name of the object in storage.

    Returns:
        UploadResponse: Metadata about the uploaded object.
    """
    # Get configured storage client via helper
    client = ManagedStorageClient().get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Determine if source is a file path or byte stream
    if isinstance(source_path, str) and os.path.isfile(source_path):
        blob.upload_from_filename(source_path)
    else:
        blob.upload_from_string(source_path)

    metadata = blob.metadata or {}
    # Preserve existing metadata and add service identifier
    blob.metadata = {**metadata, "uploaded-by": "service-integration"}
    blob.patch()

    return UploadResponse(blob_name=destination_blob_name, size=blob.size, updated=blob.updated)
