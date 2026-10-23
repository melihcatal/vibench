"""
Read object metadata or head information from managed object storage (AWS S3).

Uses boto3 S3 head_object to retrieve metadata without downloading the object.
"""

from typing import Optional

from botocore.exceptions import ClientError

from storage_client import get_s3_client, get_bucket_name, validate_object_key
from storage_models import ObjectMetadataResponse


def get_object_metadata(
    key: str,
    bucket: Optional[str] = None,
    version_id: Optional[str] = None,
    s3_client=None,
) -> ObjectMetadataResponse:
    """
    Retrieve metadata for an S3 object using head_object.

    Args:
        key: S3 object key (path within the bucket)
        bucket: Target S3 bucket name
        version_id: Specific object version (for versioned buckets)
        s3_client: Pre-configured boto3 S3 client

    Returns:
        ObjectMetadataResponse with object metadata
    """
    validate_object_key(key)
    bucket_name = get_bucket_name(bucket)
    client = s3_client or get_s3_client()

    params = {
        "Bucket": bucket_name,
        "Key": key,
    }
    if version_id:
        params["VersionId"] = version_id

    try:
        response = client.head_object(**params)
        return ObjectMetadataResponse.from_s3_head(
            bucket=bucket_name,
            key=key,
            head_response=response,
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "404" or error_code == "NoSuchKey":
            return ObjectMetadataResponse.not_found(bucket=bucket_name, key=key)
        raise


def get_object_content_type(
    key: str,
    bucket: Optional[str] = None,
    s3_client=None,
) -> Optional[str]:
    """
    Retrieve only the content type of an S3 object.

    Args:
        key: S3 object key
        bucket: Target S3 bucket name
        s3_client: Pre-configured boto3 S3 client

    Returns:
        Content type string or None if object not found
    """
    metadata = get_object_metadata(key=key, bucket=bucket, s3_client=s3_client)
    return metadata.content_type if metadata.exists else None


def object_exists(
    key: str,
    bucket: Optional[str] = None,
    s3_client=None,
) -> bool:
    """
    Check if an object exists in the S3 bucket.

    Args:
        key: S3 object key
        bucket: Target S3 bucket name
        s3_client: Pre-configured boto3 S3 client

    Returns:
        True if object exists, False otherwise
    """
    metadata = get_object_metadata(key=key, bucket=bucket, s3_client=s3_client)
    return metadata.exists


def get_object_size(
    key: str,
    bucket: Optional[str] = None,
    s3_client=None,
) -> Optional[int]:
    """
    Retrieve the size of an S3 object in bytes.

    Args:
        key: S3 object key
        bucket: Target S3 bucket name
        s3_client: Pre-configured boto3 S3 client

    Returns:
        Object size in bytes or None if object not found
    """
    metadata = get_object_metadata(key=key, bucket=bucket, s3_client=s3_client)
    return metadata.content_length if metadata.exists else None
