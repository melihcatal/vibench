import os
from google.cloud import storage
from typing import Dict, Any

def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: str, content_type: str = "application/json") -> Dict[str, Any]:
    """
    Archives an exported document snapshot or attachment in Google Cloud Storage.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(data, content_type=content_type)
        return {"status": "success", "bucket": bucket_name, "blob": destination_blob_name, "message": "File uploaded successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to upload to GCS: {e}"}

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_STORAGE_BUCKET to be set up)
    # Set a dummy bucket name for local testing if not using actual GCP project
    BUCKET_NAME = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "your-gcs-bucket-name")
    
    sample_document_data = "'{'id': 'doc_snapshot_1', 'content': 'This is a snapshot of document content.'}'"
    destination_path = "archives/document_snapshots/doc_snapshot_1.json"

    if BUCKET_NAME == "your-gcs-bucket-name":
        print("Please set GOOGLE_CLOUD_STORAGE_BUCKET environment variable for actual archiving.")
        print("Skipping actual upload for demonstration.")
        result = {"status": "skipped", "message": "GCS bucket not configured."}
    else:
        result = archive_document_snapshot(BUCKET_NAME, destination_path, sample_document_data, "application/json")

    print(f"Archive result: {result}")
