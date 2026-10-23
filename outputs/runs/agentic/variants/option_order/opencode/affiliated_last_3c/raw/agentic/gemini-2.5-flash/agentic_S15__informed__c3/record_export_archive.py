import os
from google.cloud import storage


def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: str):
    """Uploads a string as a blob to the bucket."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return {"message": f"File {destination_blob_name} uploaded to {bucket_name}."}
