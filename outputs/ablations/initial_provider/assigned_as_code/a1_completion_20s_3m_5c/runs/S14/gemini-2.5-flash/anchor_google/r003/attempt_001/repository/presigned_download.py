from datetime import timedelta

from google.cloud import storage
from storage_client import get_storage_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(payload: PresignedDownloadRequest, config=None):
    config = config or {}
    client = get_storage_client(config["project_id"])
    bucket = client.bucket(payload.bucket_name)
    blob = bucket.blob(payload.object_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(seconds=payload.expiration_seconds),
        method="GET",
    )
    return PresignedDownloadResponse(url=url)
