import logging
from storage_client import StorageClient
from storage_models import UploadObjectRequest, UploadObjectResponse

logger = logging.getLogger(__name__)


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    """Uploads a file or byte stream to AWS S3 managed object storage."""
    s3_client = StorageClient().get_client()

    try:
        response = s3_client.put_object(
            Bucket=request.bucket_name,
            Key=request.object_key,
            Body=request.data,
            Metadata=request.metadata,
        )
        etag = response.get("ETag", "").strip('"')
        version_id = response.get("VersionId")
        logger.info(
            f"Successfully uploaded object {request.object_key} to bucket {request.bucket_name}"
        )
        return UploadObjectResponse(etag=etag, version_id=version_id)
    except Exception as e:
        logger.error(
            f"Error uploading object {request.object_key} to bucket {request.bucket_name}: {e}"
        )
        raise
