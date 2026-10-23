import os
from datetime import datetime, timedelta
from storage_client import ManagedClient


def create_presigned_download_url(
    bucket_name: str, object_key: str, expiration_hours: int = 1
) -> str:
    """Create a time‑limited signed URL for downloading an object.

    The URL is valid for `expiration_hours` hours from now. The underlying
    service is Backblaze B2 Cloud Storage (b2sdk). Credentials are read from
    B2_ACCOUNT_ID and B2_APPLICATION_KEY environment variables.
    """
    client = ManagedClient()
    expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
    return client.generate_presigned_url(
        "download", bucket_name, object_key, expires_at=expires_at
    )
