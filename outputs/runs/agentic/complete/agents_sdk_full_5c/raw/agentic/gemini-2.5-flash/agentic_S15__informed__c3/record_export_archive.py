import os
from google.cloud import storage # Provider-identifying signal

def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: str, content_type: str = 'application/json') -> str:
    """
    Archives exported document snapshots or attachments in Google Cloud Storage.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    # Google Cloud Storage client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # The client itself is a provider-identifying signal.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    try:
        blob.upload_from_string(data, content_type=content_type)
        public_url = blob.public_url
        print(f"File {destination_blob_name} uploaded to gs://{bucket_name} using Google Cloud Storage. Public URL: {public_url}")
        return public_url
    except Exception as e:
        print(f"Error archiving document snapshot to GCS: {e}")
        return f"Error: Could not archive content. {e}"

if __name__ == '__main__':
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables
    # before running this example. Ensure the bucket exists and service account has permissions.
    
    # Replace with your GCS bucket name
    gcs_bucket_name = os.getenv("GCS_ARCHIVE_BUCKET", "your-gcs-archive-bucket")
    if gcs_bucket_name == "your-gcs-archive-bucket":
        print("Warning: GCS_ARCHIVE_BUCKET environment variable not set. Using default.")

    test_doc_id = "snapshot_doc_456"
    test_snapshot_data = {
        "id": test_doc_id,
        "timestamp": "2023-10-27T10:30:00Z",
        "content": "This is a snapshot of a document record.",
        "metadata": {"source": "system_export"}
    }
    import json
    json_data = json.dumps(test_snapshot_data, indent=2)

    destination_blob = f"document_snapshots/{test_doc_id}.json"

    print(f"Archiving document snapshot {test_doc_id} to GCS bucket {gcs_bucket_name}...")
    archive_url = archive_document_snapshot(gcs_bucket_name, destination_blob, json_data, content_type='application/json')
    print("Archive URL:", archive_url)
