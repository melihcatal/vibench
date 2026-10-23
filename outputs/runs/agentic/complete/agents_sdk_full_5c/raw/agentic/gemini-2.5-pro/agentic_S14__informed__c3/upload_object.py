from google.cloud import storage
import os
from .storage_client import get_bucket

def upload_file(object_name: str, file_path: str):
    """
    Uploads a file to a Google Cloud Storage bucket.

    Args:
        object_name (str): The name to give the object in the bucket.
        file_path (str): The local path to the file to upload.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    bucket = get_bucket()
    blob = bucket.blob(object_name)

    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to {object_name}.")
    return f"gs://{bucket.name}/{object_name}"
