import os
from google.cloud import storage


def archive_metric_snapshot(bucket_name, destination_blob_name, data):
    client = storage.Client(
        credentials=None
    )  # GOOGLE_APPLICATION_CREDENTIALS will be used automatically
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data, content_type="application/json")
    return f"gs://{bucket_name}/{destination_blob_name}"
