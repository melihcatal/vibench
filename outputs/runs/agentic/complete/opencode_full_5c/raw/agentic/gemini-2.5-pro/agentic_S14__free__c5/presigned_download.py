import datetime
from storage_client import get_storage_client, get_gcs_bucket_name
from storage_models import PresignedUrlResponse


def create_presigned_download_url(
    object_name: str, expiration_seconds: int = 3600
) -> PresignedUrlResponse:
    """
    Generates a presigned URL to download an object from Google Cloud Storage.

    Args:
        object_name: The name of the object in the bucket.
        expiration_seconds: Time in seconds for the presigned URL to remain valid.

    Returns:
        A PresignedUrlResponse containing the object name and the generated URL.
    """
    storage_client = get_storage_client()
    bucket_name = get_gcs_bucket_name()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(seconds=expiration_seconds),
        method="GET",
    )

    return PresignedUrlResponse(
        object_name=object_name, url=url, expiration_seconds=expiration_seconds
    )
