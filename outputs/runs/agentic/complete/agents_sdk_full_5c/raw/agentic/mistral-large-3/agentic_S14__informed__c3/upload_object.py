import os
from storage_client import get_storage_client

def upload_object(bucket_name: str, object_key: str, file_path: str = None, data_bytes: bytes = None) -> dict:
    """
    Uploads a file or byte stream to Google Cloud Storage.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_key)

    if file_path:
        blob.upload_from_filename(file_path)
    elif data_bytes:
        blob.upload_from_string(data_bytes)
    else:
        raise ValueError("Either file_path or data_bytes must be provided.")

    return {
        "bucket": bucket_name,
        "object_key": object_key,
        "public_url": blob.public_url,
        "size": blob.size
    }