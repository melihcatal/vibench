from google.cloud import storage  # Provider-identifying signal
import os


def archive_metric_snapshot(
    bucket_name: str, destination_blob_name: str, source_file_name: str
):
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}."
    )
