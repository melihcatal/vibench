# presigned_download.py
import os
from storage_client import ManagedStorageClient
from storage_models import PresignResponse

def presigned_download_url(bucket: str, object_key: str, expires_seconds: int = 3600) -> PresignResponse:
    """Create a time‑limited signed download URL for an object stored in managed object storage.

    Args:
        bucket: Bucket/container name.
        object_key: Object's key/path.
        expires_seconds: Seconds until the URL expires.

    Returns:
        PresignResponse containing the signed URL.
    """
    client = ManagedStorageClient()
    url = client.generate_presigned_url(bucket, object_key, expires_in=expires_seconds)
    return PresignResponse(url=url)
