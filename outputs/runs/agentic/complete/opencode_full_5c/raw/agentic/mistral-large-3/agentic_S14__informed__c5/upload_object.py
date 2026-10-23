from google.cloud import storage
import os
from typing import Union, BinaryIO
from dataclasses import dataclass


@dataclass
class UploadResponse:
    bucket_name: str
    object_name: str
    public_url: str
    size_bytes: int


def upload_object(
    bucket_name: str,
    object_name: str,
    data: Union[bytes, BinaryIO],
    content_type: str = None,
    metadata: dict = None,
) -> UploadResponse:
    """
    Uploads a file or byte stream to Google Cloud Storage.

    Args:
        bucket_name: Name of the GCS bucket.
        object_name: Name of the object in the bucket.
        data: File data as bytes or a file-like object.
        content_type: Optional MIME type of the file.
        metadata: Optional metadata dictionary to attach to the object.

    Returns:
        UploadResponse containing bucket, object name, public URL, and size.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    if isinstance(data, bytes):
        blob.upload_from_string(data, content_type=content_type, metadata=metadata)
        size_bytes = len(data)
    else:
        blob.upload_from_file(data, content_type=content_type, metadata=metadata)
        data.seek(0, os.SEEK_END)
        size_bytes = data.tell()
        data.seek(0)

    blob.make_public()
    return UploadResponse(
        bucket_name=bucket_name,
        object_name=object_name,
        public_url=blob.public_url,
        size_bytes=size_bytes,
    )
