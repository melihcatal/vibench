from datetime import timedelta

from storage_client import get_bucket


def create_presigned_download_url(bucket: str, object_name: str, expires_in_seconds: int = 3600) -> str:
    blob = get_bucket(bucket).blob(object_name)
    return blob.generate_signed_url(expiration=timedelta(seconds=expires_in_seconds), method="GET")
