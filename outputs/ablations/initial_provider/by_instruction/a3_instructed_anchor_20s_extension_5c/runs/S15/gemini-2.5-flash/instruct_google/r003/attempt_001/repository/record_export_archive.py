from google.cloud import storage
import os

def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: bytes) -> str:
    """
    Archives exported document snapshots or attachments in Google Cloud Storage.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(data, content_type="application/json") # Assuming JSON snapshot
        return f"gs://{bucket_name}/{destination_blob_name}"
    except Exception as e:
        print(f"Error archiving document to GCS: {e}")
        return ""

# Provider-identifying signal: google.cloud.storage
