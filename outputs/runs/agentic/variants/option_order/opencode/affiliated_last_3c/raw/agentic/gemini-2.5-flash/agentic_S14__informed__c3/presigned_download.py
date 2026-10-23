from storage_client import get_bucket
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    """Creates a time-limited signed download URL for a stored object in Google Cloud Storage."""
    bucket = get_bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    url = blob.generate_signed_url(expiration=request.expiration_seconds)

    return PresignedDownloadResponse(url=url)
