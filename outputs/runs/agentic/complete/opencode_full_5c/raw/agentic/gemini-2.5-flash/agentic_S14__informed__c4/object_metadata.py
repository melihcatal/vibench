import logging
from storage_client import get_s3_client
from storage_models import ObjectMetadataResponse

logger = logging.getLogger(__name__)


def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadataResponse:
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return ObjectMetadataResponse(
            content_length=response["ContentLength"],
            content_type=response["ContentType"],
            last_modified=response["LastModified"].isoformat(),
            e_tag=response["ETag"].strip('"'),
            metadata=response.get("Metadata", {}),
        )
    except s3_client.exceptions.NoSuchKey:
        logger.warning(f"Object {object_key} not found in bucket {bucket_name}.")
        raise FileNotFoundError(f"Object {object_key} not found.")
    except Exception as e:
        logger.error(
            f"Error getting metadata for object {object_key} in bucket {bucket_name}: {e}"
        )
        raise
