import logging
from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse

logger = logging.getLogger(__name__)


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3_client = get_s3_client()
    try:
        response = s3_client.put_object(
            Bucket=request.bucket_name, Key=request.object_key, Body=request.data
        )
        return UploadObjectResponse(
            e_tag=response["ETag"].strip('"'), version_id=response.get("VersionId")
        )
    except Exception as e:
        logger.error(
            f"Error uploading object {request.object_key} to bucket {request.bucket_name}: {e}"
        )
        raise
