from google.cloud import storage
import os

def record_export_archive(bucket_name: str, destination_blob_name: str, source_file_path: str):
    """Archives exported document snapshots or attachments in Google Cloud Storage.

    Args:
        bucket_name (str): The name of your Cloud Storage bucket.
        destination_blob_name (str): The ID of your GCS object (e.g., "snapshot/document_id.json").
        source_file_path (str): The path to the file to upload (e.g., "/tmp/document_snapshot.json").
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to {destination_blob_name} in bucket {bucket_name} using Google Cloud Storage.")
