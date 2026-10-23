from datetime import timedelta

from google.cloud import storage

from storage_client import get_bucket, get_object_path
from storage_models import DownloadUrlResponse


def presigned_download(bucket: str, key: str, expires_in: int = 900) -> DownloadUrlResponse:
    bucket_client = get_bucket(bucket)
    blob = bucket_client.blob(get_object_path(key))
    url = blob.generate_signed_url(version="v4", expiration=timedelta(seconds=expires_in), method="GET")
    return DownloadUrlResponse(bucket=bucket, key=key, url=url, expires_in=expires_in)
