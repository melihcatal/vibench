import os
from google.cloud import storage


def archive_image_asset(
    bucket_name: str, destination_blob_name: str, data: bytes
) -> str:
    """
    Archives image-analysis artifacts and derived captions in Google Cloud Storage.
    Relies on GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return f"gs://{bucket_name}/{destination_blob_name}"
