from google.cloud import storage

from storage_client import get_storage_client
from storage_models import DownloadUrlRequest


def presigned_download(request: DownloadUrlRequest) -> str:
    client = get_storage_client()
    bucket = client.bucket(request.bucket)
    blob = bucket.blob(request.name)
    return blob.generate_signed_url(version="v4", expiration=request.expiration_seconds, method="GET")
