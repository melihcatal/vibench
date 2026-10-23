"""
Read object metadata (HEAD) from Amazon S3 managed object storage.

Uses the boto3 SDK to retrieve object head information from an Amazon
Simple Storage Service (S3) bucket, including content type, size, ETag,
last-modified timestamp, storage class, and user-defined metadata.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import create_s3_client, validate_bucket_exists
from storage_models import (
    ObjectMetadataRequest,
    ObjectMetadataResponse,
    normalize_s3_metadata,
    parse_last_modified,
)

logger = logging.getLogger(__name__)


def get_object_metadata(
    bucket: str,
    key: str,
    *,
    version_id: Optional[str] = None,
    s3_client: Optional[boto3.client] = None,
) -> ObjectMetadataResponse:
    """
    Retrieve metadata for an object stored in Amazon S3 using head_object.

    Args:
        bucket: S3 bucket containing the object.
        key: Object key within the bucket.
        version_id: Optional specific object version to inspect.
        s3_client: Optional pre-created boto3 S3 client.

    Returns:
        ObjectMetadataResponse with all available head-object attributes.

    Raises:
        ValueError: If the bucket doesn't exist.
        ClientError: If the object doesn't exist or on API failure.
    """
    client = s3_client or create_s3_client()

    if not validate_bucket_exists(client, bucket):
        raise ValueError(f"Bucket '{bucket}' does not exist or is not accessible.")

    request = ObjectMetadataRequest(
        bucket=bucket,
        key=key,
        version_id=version_id,
    )

    head_params: dict[str, str] = {
        "Bucket": request.bucket,
        "Key": request.key,
    }
    if version_id:
        head_params["VersionId"] = version_id

    try:
        head = client.head_object(**head_params)
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "")
        if error_code == "404":
            logger.warning("Object not found: s3://%s/%s", bucket, key)
        else:
            logger.error(
                "Failed to retrieve metadata for s3://%s/%s: %s",
                bucket,
                key,
                exc,
            )
        raise

    raw_metadata = head.get("Metadata", {})
    normalized_metadata = normalize_s3_metadata(raw_metadata)

    # Also check for any x-amz-meta- prefixed keys in the response headers
    response_headers = head.get("ResponseMetadata", {}).get("HTTPHeaders", {})
    for hdr_key, hdr_val in response_headers.items():
        lower_hdr = hdr_key.lower()
        if lower_hdr.startswith("x-amz-meta-") and lower_hdr not in raw_metadata:
            meta_key = lower_hdr[len("x-amz-meta-"):]
            if meta_key not in normalized_metadata:
                normalized_metadata[meta_key] = str(hdr_val)

    last_modified = head.get("LastModified")
    if last_modified is not None and not isinstance(last_modified, datetime):
        last_modified = parse_last_modified(last_modified)
    if last_modified is not None and last_modified.tzinfo is None:
        last_modified = last_modified.replace(tzinfo=timezone.utc)

    result = ObjectMetadataResponse(
        bucket=bucket,
        key=key,
        content_type=head.get("ContentType", ""),
        content_length=head.get("ContentLength", 0),
        etag=head.get("ETag", "").strip('"'),
        last_modified=last_modified,
        storage_class=head.get("StorageClass", "STANDARD"),
        version_id=head.get("VersionId"),
        metadata=normalized_metadata,
        content_encoding=head.get("ContentEncoding"),
        cache_control=head.get("CacheControl"),
        content_language=head.get("ContentLanguage"),
    )
    logger.info(
        "Retrieved metadata for s3://%s/%s: %d bytes, %s",
        bucket,
        key,
        result.content_length,
        result.content_type,
    )
    return result


def object_exists(
    bucket: str,
    key: str,
    *,
    s3_client: Optional[boto3.client] = None,
) -> bool:
    """
    Check whether an object exists in Amazon S3.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        s3_client: Optional pre-created boto3 S3 client.

    Returns:
        True if the object exists, False otherwise.
    """
    try:
        get_object_metadata(bucket, key, s3_client=s3_client)
        return True
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "")
        if error_code in ("404", "NoSuchKey"):
            return False
        raise


def get_object_size(
    bucket: str,
    key: str,
    *,
    s3_client: Optional[boto3.client] = None,
) -> int:
    """
    Return the size in bytes of an object in Amazon S3.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        s3_client: Optional pre-created boto3 S3 client.

    Returns:
        Content length in bytes.
    """
    meta = get_object_metadata(bucket, key, s3_client=s3_client)
    return meta.content_length
