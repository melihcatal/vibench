from datetime import timedelta

from google.cloud import storage

from storage_client import get_bucket
from storage_models import SignedUrlResult, normalize_object_name


def presigned_download(bucket_name: str, object_name: str, expires_in_seconds: int = 3600) -> dict:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(normalize_object_name(object_name))
    url = blob.generate_signed_url(version="v4", expiration=timedelta(seconds=expires_in_seconds), method="GET")
    return SignedUrlResult(url=url, bucket=bucket_name, name=blob.name, expires_in=expires_in_seconds).to_dict()
