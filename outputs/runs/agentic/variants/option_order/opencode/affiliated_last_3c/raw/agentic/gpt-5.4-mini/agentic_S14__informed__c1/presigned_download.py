from datetime import timedelta

from google.cloud import storage

from storage_client import get_bucket, get_storage_client, load_storage_config
from storage_models import normalize_object_name


def create_presigned_download_url(
    object_name: str, expires_in_seconds: int = 900
) -> str:
    config = load_storage_config()
    client: storage.Client = get_storage_client()
    bucket = get_bucket(client, config.bucket_name)
    blob = bucket.blob(normalize_object_name(object_name))
    return blob.generate_signed_url(
        version="v4", expiration=timedelta(seconds=expires_in_seconds), method="GET"
    )
