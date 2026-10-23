from google.cloud import storage
from datetime import timedelta
from storage_client import get_storage_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def generate_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    """Generate a time-limited signed download URL for a Google Cloud Storage object."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_key)

    url = blob.generate_signed_url(
        expiration=request.expiration or timedelta(hours=1),
        version="v4"
    )

    return PresignedDownloadResponse(
        bucket_name=request.bucket_name,
        object_key=request.object_key,
        presigned_url=url,
        expires_at=request.expiration
    )