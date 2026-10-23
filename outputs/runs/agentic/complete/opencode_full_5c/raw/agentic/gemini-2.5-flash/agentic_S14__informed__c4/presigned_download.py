import logging
from storage_client import get_s3_client
from storage_models import DownloadUrlResponse

logger = logging.getLogger(__name__)


def create_presigned_download_url(
    bucket_name: str, object_key: str, expiration: int = 3600
) -> DownloadUrlResponse:
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return DownloadUrlResponse(presigned_url=response)
    except Exception as e:
        logger.error(
            f"Error generating presigned URL for object {object_key} in bucket {bucket_name}: {e}"
        )
        raise
