import os
from google.cloud import storage


def archive_document_snapshot(
    bucket_name: str, destination_blob_name: str, data: bytes
):
    """Archives exported document snapshots or attachments in Google Cloud Storage.

    Args:
        bucket_name (str): The name of the GCS bucket.
        destination_blob_name (str): The name of the blob (file) to create in the bucket.
        data (bytes): The content of the document/snapshot to upload as bytes.

    Returns:
        str: The public URL of the archived object.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    # Make the blob publicly viewable (optional, depends on use case)
    # blob.make_public()

    return blob.public_url
