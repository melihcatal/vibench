import os
from google.cloud import storage


def archive_document_snapshot(
    bucket_name: str, destination_blob_name: str, data: str
) -> str:
    # Google Cloud Storage uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    # The client creation `storage.Client()` identifies the provider.
    # No explicit GOOGLE_APPLICATION_CREDENTIALS check needed, as the SDK handles it implicitly via environment variables or gcloud cli.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data)

    return f"gs://{bucket_name}/{destination_blob_name}"
