import os
from google.cloud import storage
from typing import Union

def archive_metric_snapshot(
    bucket_name: str,
    destination_blob_name: str,
    data_to_archive: Union[str, bytes],
) -> str:
    """Archives exported metric snapshots in Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    if isinstance(data_to_archive, str):
        blob.upload_from_string(data_to_archive, content_type='application/json') # Assuming JSON content
    elif isinstance(data_to_archive, bytes):
        blob.upload_from_string(data_to_archive, content_type='application/octet-stream')
    else:
        raise ValueError("data_to_archive must be a string or bytes.")

    # The Google Cloud Storage (storage.googleapis.com) is used here.
    return f"gs://{bucket_name}/{destination_blob_name}"
