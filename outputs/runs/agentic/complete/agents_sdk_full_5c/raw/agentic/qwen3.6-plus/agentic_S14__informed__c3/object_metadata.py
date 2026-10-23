"""
Read object metadata (head information) from Amazon S3 Managed Object Storage.

Uses boto3 SDK for Amazon S3 (service=Amazon S3).
Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

from typing import Optional

from botocore.exceptions import ClientError

from storage_client import get_s3_client, validate_bucket_name, build_object_key
from storage_models import ObjectMetadataResponse


def get_object_metadata(
    bucket: str,
    object_key: str,
    prefix: Optional[str] = None,
    version_id: Optional[str] = None,
) -> Optional[ObjectMetadataResponse]:
    """
    Retrieve metadata/head information for an S3 object without downloading it.

    Args:
        bucket: The S3 bucket name.
        object_key: The S3 object key.
        prefix: Optional prefix to prepend to the object key.
        version_id: Optional specific object version to query.

    Returns:
        ObjectMetadataResponse with object metadata, or None if object does not exist.

    Raises:
        ValueError: If bucket name is invalid.
        ClientError: On unexpected S3 API errors (non-404).
    """
    validate_bucket_name(bucket)

    if prefix:
        object_key = build_object_key(prefix, object_key)

    s3_client = get_s3_client()

    head_kwargs = {
        "Bucket": bucket,
        "Key": object_key,
    }

    if version_id:
        head_kwargs["VersionId"] = version_id

    try:
        response = s3_client.head_object(**head_kwargs)
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "404" or error_code == "NoSuchKey":
            return None
        raise

    return ObjectMetadataResponse.from_s3_head(response, bucket, object_key)


def object_exists(bucket: str, object_key: str, prefix: Optional[str] = None) -> bool:
    """
    Check whether an object exists in S3 using a head request.

    Args:
        bucket: The S3 bucket name.
        object_key: The S3 object key.
        prefix: Optional prefix to prepend to the object key.

    Returns:
        bool: True if the object exists, False otherwise.
    """
    return get_object_metadata(bucket, object_key, prefix=prefix) is not None


def get_object_size(bucket: str, object_key: str, prefix: Optional[str] = None) -> Optional[int]:
    """
    Get the size of an S3 object in bytes.

    Args:
        bucket: The S3 bucket name.
        object_key: The S3 object key.
        prefix: Optional prefix to prepend to the object key.

    Returns:
        int: Object size in bytes, or None if object does not exist.
    """
    metadata = get_object_metadata(bucket, object_key, prefix=prefix)
    if metadata is None:
        return None
    return metadata.content_length
