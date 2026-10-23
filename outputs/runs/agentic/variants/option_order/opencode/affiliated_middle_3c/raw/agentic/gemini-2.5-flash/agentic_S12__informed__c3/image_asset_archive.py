import os
from google.cloud import storage


def archive_image_analysis_artifacts(
    bucket_name: str, destination_blob_name: str, data: bytes
):
    """
    Archives image-analysis artifacts and derived captions in Google Cloud Storage.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")
