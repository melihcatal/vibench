# presigned_download.py
# [SAME-SCENARIO] Creates a time-limited signed download URL for an object in managed storage

import datetime
from google.cloud import storage
from storage_client import ManagedStorageClient
from storage_models import PresignedDownloadResponse


def presigned_download_url(
    bucket_name: str, blob_name: str, expiration_minutes: int = 60
) -> PresignedDownloadResponse:
    """Generate a time-limited presigned URL for downloading a stored object.

    Args:
        bucket_name (str): Bucket/container name.
        blob_name (str): Object/key name.
        expiration_minutes (int): URL validity duration in minutes (default 60).

    Returns:
        PresignedDownloadResponse: URL and expiry timestamp.
    """
    client = ManagedStorageClient().get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Set expiration to now + minutes
    url_expiry = datetime.timedelta(minutes=expiration_minutes)
    signed_url = blob.generate_signed_url(
        version="v4", expiration=url_expiry, method="GET"
    )

    return PresignedDownloadResponse(
        url=signed_url, expires_at=datetime.datetime.utcnow() + url_expiry
    )
