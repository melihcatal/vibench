from datetime import timedelta

from storage_client import get_bucket
from storage_models import normalize_object_name


def create_presigned_download_url(bucket: str, object_name: str, expiration_seconds: int = 900) -> str:
    blob = get_bucket(bucket).blob(normalize_object_name(object_name))
    return blob.generate_signed_url(expiration=timedelta(seconds=expiration_seconds), method="GET", version="v4")
