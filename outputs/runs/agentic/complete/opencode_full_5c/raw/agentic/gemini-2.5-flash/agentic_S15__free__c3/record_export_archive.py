import os
from google.cloud import storage


def archive_document_snapshot(
    data: bytes, destination_blob_name: str, bucket_name: str
) -> str:
    """
    Archives exported document snapshots or attachments in Google Cloud Storage.
    `data` should be the content of the file (e.g., JSON string encoded to bytes).
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data, content_type="application/json")  # Assuming JSON data

    return blob.public_url
