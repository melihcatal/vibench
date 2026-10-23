from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    """Creates a time-limited signed download URL for a stored object in AWS S3.

    Args:
        request: A PresignedDownloadRequest containing bucket, key, and expiration.

    Returns:
        A PresignedDownloadResponse with the generated URL.
    """
    s3_client = get_s3_client()

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': request.bucket_name, 'Key': request.object_key},
        ExpiresIn=request.expires_in_seconds
    )

    return PresignedDownloadResponse(url=url)
