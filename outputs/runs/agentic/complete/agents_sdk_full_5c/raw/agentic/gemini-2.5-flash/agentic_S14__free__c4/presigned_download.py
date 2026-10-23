from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

def create_presigned_download_url(
    request: PresignedDownloadRequest
) -> PresignedDownloadResponse:
    """
    Creates a time-limited signed download URL for a stored object in AWS S3.
    """
    s3_client = get_s3_client()

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': request.bucket_name,
                'Key': request.object_key
            },
            ExpiresIn=request.expiration_seconds
        )
        return PresignedDownloadResponse(
            success=True,
            message="Presigned URL generated successfully",
            presigned_url=presigned_url
        )
    except Exception as e:
        return PresignedDownloadResponse(success=False, message=f"Error generating presigned URL: {str(e)}")
