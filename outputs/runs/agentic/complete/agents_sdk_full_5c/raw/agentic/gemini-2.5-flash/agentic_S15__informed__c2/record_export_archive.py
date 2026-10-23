import os
from google.cloud import storage

def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: str):
    """Archives exported document snapshots or attachments in Google Cloud Storage.

    Args:
        bucket_name: The name of your Cloud Storage bucket.
        destination_blob_name: The path to the file in the bucket (e.g., 'snapshots/document-123.json').
        data: The string content (e.g., JSON string) to upload.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # for authentication.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    print(f"Content uploaded to {destination_blob_name} in bucket {bucket_name}.")
