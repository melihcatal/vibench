# [SAME-SCENARIO] presigned_download.py

import datetime
import boto3
from urllib.parse import urlparse

from storage_client import get_managed_storage_client


def presigned_download_url(
    bucket_name: str, object_key: str, expiration_seconds: int = 3600
) -> str:
    """Create a time‑limited presigned URL for downloading an object.

    Uses AWS S3‑compatible managed object storage (e.g., Amazon S3, MinIO).
    Returns the URL as a string.
    """
    client = get_managed_storage_client()
    # Ensure expiration is a timedelta‑compatible value.
    expiration = datetime.timedelta(seconds=expiration_seconds)
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expiration_seconds,
    )
    return url
