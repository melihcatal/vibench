import os
from google.cloud import storage


def archive_export_snapshot(
    bucket_name: str, destination_blob_name: str, file_content: bytes
) -> Dict[str, Any]:
    storage_client = storage.Client()  # Google Cloud Storage
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(file_content)

    return {
        "status": "success",
        "bucket_name": bucket_name,
        "blob_name": destination_blob_name,
        "public_url": blob.public_url,
    }
