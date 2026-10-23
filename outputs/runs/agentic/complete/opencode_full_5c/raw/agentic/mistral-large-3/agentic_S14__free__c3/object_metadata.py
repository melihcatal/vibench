from typing import Dict, Optional

from boto3 import client
from botocore.exceptions import ClientError

from storage_client import get_storage_client
from storage_models import ObjectMetadataResponse


def get_object_metadata(
    bucket_name: str,
    object_key: str,
) -> ObjectMetadataResponse:
    """
    Retrieves metadata for an object in AWS S3.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path of the object in the bucket.

    Returns:
        ObjectMetadataResponse containing metadata and head information.

    Raises:
        ClientError: If the metadata retrieval fails.
    """
    s3_client = get_storage_client()

    try:
        head = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        metadata = {
            "ContentType": head.get("ContentType"),
            "ContentLength": head.get("ContentLength"),
            "ETag": head.get("ETag"),
            "LastModified": head.get("LastModified"),
            "Metadata": head.get("Metadata", {}),
            "StorageClass": head.get("StorageClass"),
        }

        return ObjectMetadataResponse(metadata=metadata)
    except ClientError as e:
        raise ClientError(
            error_response={
                "Error": {
                    "Code": e.response["Error"]["Code"],
                    "Message": e.response["Error"]["Message"],
                }
            },
            operation_name="get_object_metadata",
        )
