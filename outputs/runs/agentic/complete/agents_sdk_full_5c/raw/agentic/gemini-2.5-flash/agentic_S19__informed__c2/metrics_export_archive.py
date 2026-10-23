from google.cloud import storage
import os

def archive_metric_snapshot(
    bucket_name: str,
    destination_blob_name: str,
    data_to_archive: str,
):
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data_to_archive, content_type='application/json')

    print(f"Metric snapshot {destination_blob_name} uploaded to {bucket_name}.")
