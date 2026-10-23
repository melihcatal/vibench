from google.cloud import storage
import os


def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: str):
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return {
        "status": "success",
        "bucket_name": bucket_name,
        "blob_name": destination_blob_name,
    }
