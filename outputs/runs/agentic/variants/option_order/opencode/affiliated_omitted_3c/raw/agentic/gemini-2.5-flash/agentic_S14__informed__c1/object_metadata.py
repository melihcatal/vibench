import logging
from storage_client import StorageClient
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

logger = logging.getLogger(__name__)


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    """Reads object metadata or head information from AWS S3 managed object storage."""
    s3_client = StorageClient().get_client()

    try:
        response = s3_client.head_object(
            Bucket=request.bucket_name, Key=request.object_key
        )
        # The HeadObject response contains various metadata, we'll return a subset or all of it
        metadata = {
            "ContentLength": response.get("ContentLength"),
            "ContentType": response.get("ContentType"),
            "ETag": response.get("ETag", "").strip('"'),
            "LastModified": response.get("LastModified").isoformat()
            if response.get("LastModified")
            else None,
            "VersionId": response.get("VersionId"),
            "Metadata": response.get("Metadata", {}),
        }
        logger.info(
            f"Successfully retrieved metadata for object {request.object_key} in bucket {request.bucket_name}"
        )
        return ObjectMetadataResponse(metadata=metadata)
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logger.warning(
                f"Object {request.object_key} not found in bucket {request.bucket_name}"
            )
            return ObjectMetadataResponse(metadata={})
        else:
            logger.error(
                f"Error retrieving metadata for object {request.object_key} in bucket {request.bucket_name}: {e}"
            )
            raise
    except Exception as e:
        logger.error(
            f"Error retrieving metadata for object {request.object_key} in bucket {request.bucket_name}: {e}"
        )
        raise
