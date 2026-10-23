from storage_client import get_storage_client
from typing import IO, Union


def upload_object(
    bucket_name: str, object_name: str, file_source: Union[str, IO[bytes]]
):
    """
    Uploads a file or byte stream to a Google Cloud Storage bucket.

    :param bucket_name: The name of the GCS bucket.
    :param object_name: The name of the object to create.
    :param file_source: The local file path or a file-like object to upload.
    """
    storage_client = get_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    if isinstance(file_source, str):
        blob.upload_from_filename(file_source)
    else:
        blob.upload_from_file(file_source)

    return f"gs://{bucket_name}/{object_name}"
