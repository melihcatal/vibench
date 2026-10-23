from google.cloud import storage
import os


def archive_metric_snapshot(
    bucket_name: str, destination_blob_name: str, data: str
) -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return f"Uploaded {destination_blob_name} to {bucket_name}."
