from google.cloud import storage
import os

def record_export_archive(bucket_name: str, destination_blob_name: str, data: bytes):
    """Uploads a file to the Google Cloud Storage bucket."""
    # bucket_name = "your-bucket-name"
    # destination_blob_name = "storage-object-name"
    # data = b"your document content"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return {"status": "success", "bucket": bucket_name, "blob": destination_blob_name}