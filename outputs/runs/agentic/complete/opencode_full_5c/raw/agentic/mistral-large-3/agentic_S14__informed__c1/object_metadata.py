import boto3
from botocore.exceptions import ClientError

from storage_client import get_storage_client
from storage_models import ObjectMetadataResponse


def get_object_metadata(
    bucket_name: str,
    object_key: str,
) -> ObjectMetadataResponse:
    """
    Retrieves metadata for an object in Amazon S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key of the object in the bucket.

    Returns:
        ObjectMetadataResponse containing metadata and head information.
    """
    s3_client = get_storage_client()

    try:
        response = s3_client.head_object(
            Bucket=bucket_name,
            Key=object_key,
        )

        metadata = response.get("Metadata", {})
        metadata.update(
            {
                "ContentType": response.get("ContentType"),
                "ContentLength": response.get("ContentLength"),
                "LastModified": response.get("LastModified"),
                "ETag": response.get("ETag", "").strip('"'),
                "VersionId": response.get("VersionId"),
            }
        )

        return ObjectMetadataResponse(
            object_id=object_key, metadata=metadata, provider="aws_s3"
        )
    except ClientError as e:
        raise Exception(f"Failed to retrieve object metadata: {e}")
