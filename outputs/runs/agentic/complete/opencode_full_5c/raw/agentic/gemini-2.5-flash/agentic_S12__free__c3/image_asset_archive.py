from google.cloud import storage
import os


def archive_artifact(
    bucket_name: str, source_file_name: str, destination_blob_name: str
):
    """
    Archives image-analysis artifacts and derived captions in Google Cloud Storage.
    Provider: Google Cloud Storage
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(source_file_name)

    return f"File {source_file_name} uploaded to gs://{bucket_name}/{destination_blob_name}"


def archive_text_content(bucket_name: str, content: str, destination_blob_name: str):
    """
    Archives text content (e.g., derived captions) in Google Cloud Storage.
    Provider: Google Cloud Storage
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the string content
    blob.upload_from_string(content)

    return f"Text content uploaded to gs://{bucket_name}/{destination_blob_name}"
