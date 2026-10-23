import os
from google.cloud import storage

def archive_metric_snapshot(bucket_name: str, destination_blob_name: str, data: bytes):
    """
    Archives exported metric snapshots in Google Cloud Storage.

    Args:
        bucket_name: The name of your Cloud Storage bucket.
        destination_blob_name: The desired name of the blob (file) in the bucket.
        data: The content of the metric snapshot as bytes.
    """
    # Google Cloud Storage automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # if set, or attempts to find credentials.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data, content_type='application/json') # Assuming JSON data

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")

