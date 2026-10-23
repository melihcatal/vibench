"""
Read object metadata or head information from managed object storage.

Uses AWS S3 (boto3) as the concrete managed object storage provider.
Retrieves HEAD / metadata information for objects in S3 buckets.
"""

from datetime import datetime
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import StorageClient, get_client
from storage_models import StorageObjectMetadata, parse_s3_response_to_metadata


def get_object_metadata(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    part_number: Optional[int] = None,
    client: Optional[StorageClient] = None,
) -> StorageObjectMetadata:
    """
    Retrieve metadata for an object stored in AWS S3.

    Performs a HeadObject operation to fetch metadata without downloading
    the object content itself.

    Args:
        bucket: S3 bucket name.
        key: Object key within the bucket.
        version_id: Specific object version for versioned buckets.
        part_number: For multipart objects, the specific part number.
        client: Optional pre-configured StorageClient instance.

    Returns:
        StorageObjectMetadata with all available object metadata.

    Raises:
        ClientError: If the object does not exist or access is denied.
    """
    if client is None:
        client = get_client()

    s3_client = client.get_s3_client()

    head_params: Dict[str, Any] = {
        "Bucket": bucket,
        "Key": key,
    }

    if version_id:
        head_params["VersionId"] = version_id
    if part_number is not None:
        head_params["PartNumber"] = part_number

    try:
        response = s3_client.head_object(**head_params)
        return parse_s3_response_to_metadata(response, bucket, key)

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "404" or error_code == "NoSuchKey":
            return StorageObjectMetadata(
                bucket=bucket,
                key=key,
                exists=False,
            )
        raise ClientError(
            e.response,
            f"Failed to get metadata for s3://{bucket}/{key}: {e}",
        )


def get_object_full_metadata(
    bucket: str,
    key: str,
    include_body: bool = False,
    client: Optional[StorageClient] = None,
) -> StorageObjectMetadata:
    """
    Retrieve full object metadata via GetObject (optionally including body).

    Uses S3 GetObject to retrieve metadata and optionally the object content.
    Returns metadata along with additional fields available from GetObject.

    Args:
        bucket: S3 bucket name.
        key: Object key within the bucket.
        include_body: If True, return the object body in metadata (not recommended
                     for large objects; body is accessible via metadata extra field).
        client: Optional pre-configured StorageClient instance.

    Returns:
        StorageObjectMetadata enriched with GetObject response fields.
    """
    if client is None:
        client = get_client()

    s3_client = client.get_s3_client()

    get_params = {
        "Bucket": bucket,
        "Key": key,
    }

    try:
        response = s3_client.get_object(**get_params)

        metadata = parse_s3_response_to_metadata(response, bucket, key)

        if include_body and "Body" in response:
            body = response["Body"]
            if hasattr(metadata, "__dict__"):
                metadata.extra_fields = {"body": body}

        return metadata

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "NoSuchKey":
            return StorageObjectMetadata(
                bucket=bucket,
                key=key,
                exists=False,
            )
        raise ClientError(
            e.response,
            f"Failed to get object s3://{bucket}/{key}: {e}",
        )


def object_exists(bucket: str, key: str, client: Optional[StorageClient] = None) -> bool:
    """
    Check whether an object exists in S3 without downloading it.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        client: Optional pre-configured StorageClient instance.

    Returns:
        True if the object exists, False otherwise.
    """
    try:
        metadata = get_object_metadata(bucket, key, client=client)
        return metadata.exists
    except ClientError:
        return False


def get_object_etag(bucket: str, key: str, client: Optional[StorageClient] = None) -> Optional[str]:
    """
    Get the ETag of an S3 object.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        client: Optional pre-configured StorageClient instance.

    Returns:
        ETag string or None if object doesn't exist.
    """
    metadata = get_object_metadata(bucket, key, client=client)
    return metadata.etag if metadata.exists else None


def get_object_size(bucket: str, key: str, client: Optional[StorageClient] = None) -> Optional[int]:
    """
    Get the content length of an S3 object.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        client: Optional pre-configured StorageClient instance.

    Returns:
        Content length in bytes or None if object doesn't exist.
    """
    metadata = get_object_metadata(bucket, key, client=client)
    return metadata.content_length if metadata.exists else None
