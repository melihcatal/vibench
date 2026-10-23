from storage_client import get_storage_client, get_gcs_bucket_name
from google.cloud.storage import Blob


def upload_object(file_path: str, object_name: str) -> None:
    """
    Uploads a file to a Google Cloud Storage bucket.

    Args:
        file_path: Path to the file to upload.
        object_name: The name to give the object in the bucket.
    """
    storage_client = get_storage_client()
    bucket_name = get_gcs_bucket_name()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to {bucket_name}/{object_name}.")


def upload_object_from_bytes(
    data: bytes, object_name: str, content_type: str = "application/octet-stream"
) -> None:
    """
    Uploads a byte stream to a Google Cloud Storage bucket.

    Args:
        data: The byte stream to upload.
        object_name: The name to give the object in the bucket.
        content_type: The content type of the data.
    """
    storage_client = get_storage_client()
    bucket_name = get_gcs_bucket_name()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    blob.upload_from_string(data, content_type=content_type)
    print(f"Bytes uploaded to {bucket_name}/{object_name}.")
