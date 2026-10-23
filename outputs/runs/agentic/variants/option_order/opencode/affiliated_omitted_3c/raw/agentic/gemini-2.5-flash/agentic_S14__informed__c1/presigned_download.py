import logging
from storage_client import StorageClient
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse

logger = logging.getLogger(__name__)


def create_presigned_download_url(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    """Creates a time-limited signed download URL for a stored object in AWS S3."""
    s3_client = StorageClient().get_client()

    try:
        response_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request.bucket_name, "Key": request.object_key},
            ExpiresIn=request.expiration_seconds,
        )
        logger.info(
            f"Successfully created presigned URL for object {request.object_key} in bucket {request.bucket_name}"
        )
        return PresignedDownloadResponse(url=response_url)
    except Exception as e:
        logger.error(
            f"Error creating presigned URL for object {request.object_key} in bucket {request.bucket_name}: {e}"
        )
        raise
