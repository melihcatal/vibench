from google.cloud import storage
import os

def archive_metric_snapshot(bucket_name: str, destination_blob_name: str, data: str):
    # Google Cloud Storage client automatically uses credentials from GOOGLE_APPLICATION_CREDENTIALS
    # or other standard Google Cloud authentication methods.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the string data to the blob
    blob.upload_from_string(data)

    return f"Metric snapshot '{destination_blob_name}' uploaded to Google Cloud Storage bucket '{bucket_name}'."

