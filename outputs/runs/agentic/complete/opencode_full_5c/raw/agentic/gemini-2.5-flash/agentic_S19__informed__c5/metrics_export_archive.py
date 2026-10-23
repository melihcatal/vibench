import os
from google.cloud import storage


def archive_metric_snapshot(
    bucket_name: str, destination_blob_name: str, data: str
) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return f"gs://{bucket_name}/{destination_blob_name}"
