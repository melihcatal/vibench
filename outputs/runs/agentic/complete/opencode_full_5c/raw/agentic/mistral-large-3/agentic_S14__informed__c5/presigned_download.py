from google.cloud import storage
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class PresignedDownloadResponse:
    url: str
    expires_at: datetime


def presigned_download(
    bucket_name: str, object_name: str, expiration_hours: int = 1
) -> PresignedDownloadResponse:
    """
    Creates a time-limited signed download URL for a Google Cloud Storage object.

    Args:
        bucket_name: Name of the GCS bucket.
        object_name: Name of the object in the bucket.
        expiration_hours: Number of hours until the URL expires.

    Returns:
        PresignedDownloadResponse containing the signed URL and expiration time.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
    url = blob.generate_signed_url(expiration=expires_at, version="v4")

    return PresignedDownloadResponse(url=url, expires_at=expires_at)
