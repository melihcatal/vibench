from __future__ import annotations

from datetime import timedelta

from storage_client import get_bucket


def create_presigned_download_url(bucket_name: str, object_name: str, expiration_seconds: int = 3600) -> str:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    return blob.generate_signed_url(expiration=timedelta(seconds=expiration_seconds), method="GET", version="v4")
