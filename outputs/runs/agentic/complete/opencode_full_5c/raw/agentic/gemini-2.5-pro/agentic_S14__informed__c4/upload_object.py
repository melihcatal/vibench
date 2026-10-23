from typing import IO, Union
from storage_client import get_gcs_client, get_storage_bucket
from storage_models import UploadResponse


def upload_object_to_gcs(
    bucket_name: str,
    object_name: str,
    data: Union[bytes, str, IO],
    content_type: str = "application/octet-stream",
) -> UploadResponse:
    """
    Uploads a file or byte stream to a Google Cloud Storage bucket.

    Args:
        bucket_name: The name of the GCS bucket.
        object_name: The name of the object to create.
        data: The data to upload (bytes, string, or file-like object).
        content_type: The content type of the object.

    Returns:
        An UploadResponse object with the upload details.
    """
    client = get_gcs_client()
    bucket = get_storage_bucket(client, bucket_name)
    blob = bucket.blob(object_name)

    if isinstance(data, str):
        data = data.encode("utf-8")

    if hasattr(data, "read"):
        blob.upload_from_file(data, content_type=content_type)
    else:
        blob.upload_from_string(data, content_type=content_type)

    blob.reload()

    return UploadResponse(
        bucket=bucket.name, object_name=blob.name, success=True, size=blob.size
    )
