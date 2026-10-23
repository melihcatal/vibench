import os
from typing import BinaryIO, Union

from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError


def upload_object(
    bucket_name: str,
    object_name: str,
    data: Union[bytes, BinaryIO],
    content_type: str = None,
    metadata: dict = None,
) -> str:
    """
    Uploads a file or byte stream to Google Cloud Storage.

    Args:
        bucket_name: Name of the GCS bucket.
        object_name: Name of the object to upload.
        data: File-like object or bytes to upload.
        content_type: Optional content type of the object.
        metadata: Optional metadata to attach to the object.

    Returns:
        The public URL of the uploaded object.

    Raises:
        GoogleAPIError: If the upload fails.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    if metadata:
        blob.metadata = metadata

    blob.upload_from_file(data, content_type=content_type) if hasattr(
        data, "read"
    ) else blob.upload_from_string(data, content_type=content_type)

    return f"gs://{bucket_name}/{object_name}"
