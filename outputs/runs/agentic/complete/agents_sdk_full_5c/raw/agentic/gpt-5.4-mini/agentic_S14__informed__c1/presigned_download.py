from datetime import timedelta
from typing import Optional

from storage_client import get_bucket
from storage_models import PresignedDownloadRequest


def create_presigned_download_url(
    object_name: str,
    bucket_name: Optional[str] = None,
    expiration_seconds: int = 3600,
) -> str:
    request = PresignedDownloadRequest(
        bucket_name=bucket_name,
        object_name=object_name,
        expiration_seconds=expiration_seconds,
    )
    bucket = get_bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)
    return blob.generate_signed_url(expiration=timedelta(seconds=request.expiration_seconds), version="v4", method="GET")
