import os
from typing import BinaryIO, Optional, Union

from google.cloud import storage


def upload_object(
    bucket_name: str,
    object_name: str,
    data: Union[bytes, bytearray, BinaryIO],
    content_type: Optional[str] = None,
) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    if hasattr(data, "read"):
        blob.upload_from_file(data, content_type=content_type)
    else:
        blob.upload_from_string(bytes(data), content_type=content_type)
    return f"gs://{bucket_name}/{object_name}"


def upload_from_path(
    bucket_name: str,
    object_name: str,
    file_path: str,
    content_type: Optional[str] = None,
) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(file_path, content_type=content_type)
    return f"gs://{bucket_name}/{object_name}"


if __name__ == "__main__":
    bucket = os.environ["GCS_BUCKET_NAME"]
    key = os.environ.get("GCS_OBJECT_NAME", "upload.bin")
    path = os.environ.get("GCS_FILE_PATH")
    if path:
        print(upload_from_path(bucket, key, path))
