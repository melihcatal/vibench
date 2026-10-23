from __future__ import annotations

from storage_client import get_bucket
from storage_models import PresignedDownloadRequest


def create_presigned_download_url(bucket: str, key: str, expires_in: int = 3600) -> str:
    request = PresignedDownloadRequest(bucket=bucket, key=key, expires_in=expires_in)
    blob = get_bucket(request.bucket).blob(request.key)
    return blob.generate_signed_url(version="v4", expiration=request.expires_in, method="GET")
