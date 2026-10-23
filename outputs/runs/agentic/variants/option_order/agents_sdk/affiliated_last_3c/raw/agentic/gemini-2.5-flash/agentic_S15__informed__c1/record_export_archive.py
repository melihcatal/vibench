import os
from google.cloud import storage

def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: bytes):
    """Archives exported document snapshots or attachments in Google Cloud Storage.

    Args:
        bucket_name: The name of your Cloud Storage bucket.
        destination_blob_name: The path to the file in the bucket (e.g., "snapshots/doc_id_timestamp.json").
        data: The content to upload, as bytes (e.g., JSON string encoded to bytes).
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS or default credentials are set up
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data, content_type="application/json") # Assuming JSON data

    print(f"Document snapshot uploaded to gs://{bucket_name}/{destination_blob_name}.")

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS or default credentials setup)
    # import json
    # from datetime import datetime
    #
    # bucket = "your-gcs-bucket-name" # Replace with your GCS bucket name
    # doc_id = "mydocument123"
    # timestamp = datetime.now().isoformat()
    #
    # snapshot_data = {
    #     "id": doc_id,
    #     "timestamp": timestamp,
    #     "content": "This is the content of the document to be archived."
    # }
    #
    # blob_name = f"document_archives/{doc_id}_{timestamp}.json"
    #
    # # Convert dict to JSON string, then encode to bytes
    # data_bytes = json.dumps(snapshot_data, indent=2).encode("utf-8")
    #
    # try:
    #     archive_document_snapshot(bucket, blob_name, data_bytes)
    # except Exception as e:
    #     print(f"Error archiving document: {e}")
    pass
