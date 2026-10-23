import os
from google.cloud import storage
from typing import Dict, Any

def archive_document_snapshot(bucket_name: str, destination_blob_name: str, data: str):
    # Google Cloud Storage expects GOOGLE_APPLICATION_CREDENTIALS or similar auth
    # For this example, we assume authentication is set up in the environment.
    # More info: https://cloud.google.com/docs/authentication/getting-started

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return f"gs://{bucket_name}/{destination_blob_name}"
