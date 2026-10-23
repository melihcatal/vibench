import os
from google.cloud import storage
from typing import Dict, Any


def archive_document_snapshot(
    bucket_name: str,
    destination_blob_name: str,
    file_content: str,
    content_type: str = "application/json",
) -> Dict[str, Any]:
    """
    Archives exported document snapshots or attachments in Google Cloud Storage.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(file_content, content_type=content_type)

    return {
        "bucket": bucket_name,
        "blob_name": destination_blob_name,
        "public_url": blob.public_url,
    }
