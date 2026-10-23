from google.cloud import storage
from storage_client import get_storage_client, get_bucket_name
from storage_models import PresignedDownloadResponse
from datetime import timedelta


def create_presigned_download_url(object_name: str, expires_in_seconds: int = 3600) -> PresignedDownloadResponse:
    """
    Create a time-limited signed download URL for a Google Cloud Storage object.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    url = blob.generate_signed_url(
        expiration=timedelta(seconds=expires_in_seconds),
        method="GET",
    )

    return PresignedDownloadResponse(url=url, expires_in_seconds=expires_in_seconds)