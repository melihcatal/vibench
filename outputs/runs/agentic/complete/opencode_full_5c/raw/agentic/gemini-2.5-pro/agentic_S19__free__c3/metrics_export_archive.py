import os
from google.cloud import storage


def archive_metrics_snapshot(
    bucket_name: str, source_file_name: str, destination_blob_name: str
):
    """
    Uploads a file to a Google Cloud Storage bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
