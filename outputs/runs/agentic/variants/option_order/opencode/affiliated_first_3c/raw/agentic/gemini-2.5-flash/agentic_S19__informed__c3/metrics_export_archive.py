from google.cloud import storage
import os
from typing import Dict, Any


def archive_metric_snapshot(
    bucket_name: str, destination_blob_name: str, data: str
) -> Dict[str, Any]:
    """
    Archives exported metric snapshots in Google Cloud Storage.
    Assumes GOOGLE_APPLICATION_CREDENTIALS are set for authentication.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return {
        "bucket": bucket_name,
        "blob": destination_blob_name,
        "public_url": blob.public_url,
    }
