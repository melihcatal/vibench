import os
from google.cloud import storage
from datetime import datetime


def archive_metric_snapshot(
    bucket_name: str, destination_blob_name: str, data: str
) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(
        data, content_type="application/json"
    )  # Assuming data is JSON string

    return f"gs://{bucket_name}/{destination_blob_name}"
