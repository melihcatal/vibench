from storage_client import get_storage_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(
    request: PresignedDownloadRequest
) -> PresignedDownloadResponse:
    """Creates a time-limited signed download URL for a stored object in Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    signed_url = blob.generate_signed_url(
        expiration=request.expiration_seconds,
        method='GET'
    )

    return PresignedDownloadResponse(
        signed_url=signed_url
    )
