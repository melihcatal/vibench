from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    """Creates a time-limited signed download URL for an AWS S3 stored object."""
    s3_client = get_s3_client()

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': request.bucket_name,
                'Key': request.object_key
            },
            ExpiresIn=request.expiration_seconds,
        )
        return PresignedDownloadResponse(presigned_url=presigned_url)
    except Exception as e:
        raise RuntimeError(f"Error generating presigned URL: {e}") from e
