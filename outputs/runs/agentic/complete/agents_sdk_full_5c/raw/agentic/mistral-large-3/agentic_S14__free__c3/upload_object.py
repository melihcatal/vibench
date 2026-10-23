from typing import Optional, Dict
from google.cloud import storage
from storage_client import get_storage_client, get_bucket_name
from storage_models import UploadRequest


def upload_object(
    object_name: str,
    data: bytes,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> str:
    """
    Upload a file or byte stream to Google Cloud Storage.
    Returns the object path.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    if content_type:
        blob.content_type = content_type
    if metadata:
        blob.metadata = metadata

    blob.upload_from_string(data)
    return f"gs://{bucket_name}/{object_name}"