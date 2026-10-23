import os
from storage_client import StorageClient


def upload_object(bucket_name: str, source_file_name: str, destination_blob_name: str):
    """Uploads a file to a Google Cloud Storage bucket."""
    storage_client = StorageClient.get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}."
    )


def upload_object_from_bytes(
    bucket_name: str,
    data: bytes,
    destination_blob_name: str,
    content_type: str = "application/octet-stream",
):
    """Uploads a byte stream to a Google Cloud Storage bucket."""
    storage_client = StorageClient.get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data, content_type=content_type)

    print(f"Byte stream uploaded to {destination_blob_name} in bucket {bucket_name}.")
