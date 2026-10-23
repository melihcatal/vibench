import os
from google.cloud import storage


def archive_document_snapshot(
    bucket_name: str, destination_blob_name: str, data: bytes
):
    """
    Archives exported document snapshots or attachments in Google Cloud Storage.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return {
        "status": "success",
        "bucket": bucket_name,
        "blob": destination_blob_name,
        "public_url": blob.public_url,
    }
