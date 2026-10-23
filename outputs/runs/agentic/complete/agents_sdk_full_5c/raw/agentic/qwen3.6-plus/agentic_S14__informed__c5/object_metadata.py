"""
object_metadata.py - Reads object metadata or head information from managed object storage.

Uses Amazon S3 via boto3 as the concrete managed object storage provider.
Authentication via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
"""

from typing import Optional

from botocore.exceptions import ClientError

from storage_client import get_s3_client
from storage_models import StorageObjectMetadata, normalize_s3_head_response


def get_object_metadata(
    bucket_name: str,
    object_key: str,
    version_id: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> StorageObjectMetadata:
    """
    Retrieve metadata for an object stored in Amazon S3 using head_object.

    This operation retrieves only the object's metadata without downloading
    the object content itself.

    Args:
        bucket_name: S3 bucket containing the object.
        object_key: S3 object key to retrieve metadata for.
        version_id: Optional specific version ID of the object.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        StorageObjectMetadata with normalized object metadata.

    Raises:
        ValueError: If bucket_name or object_key is empty.
        RuntimeError: If the object is not found or metadata retrieval fails.
    """
    if not bucket_name or not object_key:
        raise ValueError("Both 'bucket_name' and 'object_key' are required.")

    s3_client = get_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    head_params = {
        "Bucket": bucket_name,
        "Key": object_key,
    }

    if version_id:
        head_params["VersionId"] = version_id

    try:
        response = s3_client.head_object(**head_params)

        return normalize_s3_head_response(
            head_response=response,
            bucket_name=bucket_name,
            object_key=object_key,
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")

        if error_code == "404" or error_code == "NoSuchKey":
            raise RuntimeError(
                f"Object not found in S3: bucket='{bucket_name}', key='{object_key}'"
            ) from e

        raise RuntimeError(
            f"Failed to retrieve object metadata from S3: {error_code} - {e}"
        ) from e


def get_object_tags(
    bucket_name: str,
    object_key: str,
    version_id: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> dict:
    """
    Retrieve tags associated with an S3 object.

    Args:
        bucket_name: S3 bucket containing the object.
        object_key: S3 object key.
        version_id: Optional specific version ID of the object.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        Dictionary of tag key-value pairs.

    Raises:
        RuntimeError: If tag retrieval fails.
    """
    s3_client = get_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    tag_params = {
        "Bucket": bucket_name,
        "Key": object_key,
    }

    if version_id:
        tag_params["VersionId"] = version_id

    try:
        response = s3_client.get_object_tagging(**tag_params)
        return {tag["Key"]: tag["Value"] for tag in response.get("TagSet", [])}

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        raise RuntimeError(
            f"Failed to retrieve object tags from S3: {error_code} - {e}"
        ) from e


def object_exists(
    bucket_name: str,
    object_key: str,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> bool:
    """
    Check if an object exists in Amazon S3.

    Args:
        bucket_name: S3 bucket to check.
        object_key: S3 object key to verify.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        True if the object exists, False otherwise.
    """
    try:
        get_object_metadata(
            bucket_name=bucket_name,
            object_key=object_key,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        return True
    except RuntimeError:
        return False
