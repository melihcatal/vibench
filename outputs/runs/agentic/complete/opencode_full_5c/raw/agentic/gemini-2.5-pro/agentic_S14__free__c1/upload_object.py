import os
from storage_client import get_storage_client


def upload_object(bucket_name: str, source_file_name: str, destination_blob_name: str):
    """Uploads a file to the bucket."""
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
    return f"gs://{bucket_name}/{destination_blob_name}"


def upload_from_string(
    bucket_name: str, source_string: str, destination_blob_name: str
):
    """Uploads a string to the bucket."""
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(source_string)

    print(f"String uploaded to {destination_blob_name}.")
    return f"gs://{bucket_name}/{destination_blob_name}"
