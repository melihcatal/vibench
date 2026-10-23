from google.cloud import storage
from datetime import datetime

def archive_document_export(bucket_name: str, file_content: str, destination_blob_name: str) -> str:
    """Uploads a file to the Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(file_content)

    return f"gs://{bucket_name}/{destination_blob_name}"
