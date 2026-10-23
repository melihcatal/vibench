import os
from google.cloud import storage


def record_export_archive(
    bucket_name: str, source_file_name: str, destination_blob_name: str
):
    os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    return f"File {source_file_name} uploaded to {destination_blob_name}."
