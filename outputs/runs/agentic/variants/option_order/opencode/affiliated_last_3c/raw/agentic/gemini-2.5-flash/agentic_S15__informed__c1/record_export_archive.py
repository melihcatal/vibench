from google.cloud import storage
import os


def archive_blob(
    bucket_name: str, source_file_name: str, destination_blob_name: str
) -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # with the path to your service account key file.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    return f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}."


def archive_content(
    bucket_name: str,
    content: str,
    destination_blob_name: str,
    content_type: str = "text/plain",
) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(content, content_type=content_type)

    return f"Content uploaded to {destination_blob_name} in bucket {bucket_name}."
