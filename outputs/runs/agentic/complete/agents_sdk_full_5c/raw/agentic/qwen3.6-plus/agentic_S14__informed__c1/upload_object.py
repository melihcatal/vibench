"""
Upload a file or byte stream to Amazon S3 managed object storage.

Uses the boto3 SDK to upload objects to an Amazon Simple Storage Service (S3)
bucket. Credentials are read from AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
environment variables or the default AWS credential chain.
"""

from __future__ import annotations

import logging
import os
from typing import BinaryIO, Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import create_s3_client, validate_bucket_exists
from storage_models import UploadRequest, UploadResponse, build_s3_uri

logger = logging.getLogger(__name__)


def upload_object(
    bucket: str,
    key: str,
    *,
    content: Optional[bytes] = None,
    file_path: Optional[str] = None,
    content_type: str = "application/octet-stream",
    metadata: Optional[dict[str, str]] = None,
    storage_class: str = "STANDARD",
    acl: Optional[str] = None,
    s3_client: Optional[boto3.client] = None,
) -> UploadResponse:
    """
    Upload a file or byte stream to an Amazon S3 bucket.

    Args:
        bucket: Target S3 bucket name.
        key: Object key (path) within the bucket.
        content: Raw bytes to upload. Mutually exclusive with file_path.
        file_path: Local filesystem path to read from. Mutually exclusive with content.
        content_type: MIME content type for the stored object.
        metadata: User-defined metadata key-value pairs.
        storage_class: S3 storage class (e.g., STANDARD, INTELLIGENT_TIERING).
        acl: Optional canned ACL (e.g., 'private', 'public-read').
        s3_client: Pre-configured boto3 S3 client. Created automatically if omitted.

    Returns:
        UploadResponse with bucket, key, ETag, version ID, and S3 URI.

    Raises:
        ValueError: If neither content nor file_path is provided, or both are given.
        ClientError: On S3 API failure.
    """
    if content is not None and file_path is not None:
        raise ValueError("Provide either content or file_path, not both.")
    if content is None and file_path is None:
        raise ValueError("Either content or file_path must be provided.")

    client = s3_client or create_s3_client()

    if not validate_bucket_exists(client, bucket):
        raise ValueError(f"Bucket '{bucket}' does not exist or is not accessible.")

    extra_args: dict[str, str | dict] = {
        "ContentType": content_type,
        "StorageClass": storage_class,
    }
    if metadata:
        extra_args["Metadata"] = metadata
    if acl:
        extra_args["ACL"] = acl

    request = UploadRequest(
        bucket=bucket,
        key=key,
        content=content,
        file_path=file_path,
        content_type=content_type,
        metadata=metadata or {},
        storage_class=storage_class,
        acl=acl,
    )

    try:
        if request.content is not None:
            response = client.put_object(
                Bucket=request.bucket,
                Key=request.key,
                Body=request.content,
                **extra_args,  # type: ignore[arg-type]
            )
            content_length = len(request.content)
        elif request.file_path is not None:
            with open(request.file_path, "rb") as fh:
                response = client.put_object(
                    Bucket=request.bucket,
                    Key=request.key,
                    Body=fh,
                    **extra_args,  # type: ignore[arg-type]
                )
            content_length = os.path.getsize(request.file_path)
        else:
            raise ValueError("No content or file_path provided.")

    except ClientError as exc:
        logger.error("S3 upload failed for s3://%s/%s: %s", bucket, key, exc)
        raise

    etag = response.get("ETag", "").strip('"')
    version_id = response.get("VersionId")
    request_id = response.get("ResponseMetadata", {}).get("RequestId", "")

    result = UploadResponse(
        bucket=bucket,
        key=key,
        etag=etag,
        version_id=version_id,
        request_id=request_id,
        s3_uri=build_s3_uri(bucket, key),
        content_length=content_length,
    )
    logger.info(
        "Uploaded %d bytes to %s (ETag=%s)",
        content_length,
        result.s3_uri,
        result.etag,
    )
    return result


def upload_fileobj(
    bucket: str,
    key: str,
    fileobj: BinaryIO,
    *,
    content_type: str = "application/octet-stream",
    metadata: Optional[dict[str, str]] = None,
    storage_class: str = "STANDARD",
    acl: Optional[str] = None,
    s3_client: Optional[boto3.client] = None,
) -> UploadResponse:
    """
    Upload from an open binary file-like object using Amazon S3 upload_fileobj.

    Supports automatic multipart upload for large files.

    Args:
        bucket: Target S3 bucket name.
        key: Object key within the bucket.
        fileobj: An open binary file-like object (e.g., io.BytesIO, open file handle).
        content_type: MIME content type.
        metadata: User-defined metadata.
        storage_class: S3 storage class.
        acl: Optional canned ACL.
        s3_client: Optional pre-created boto3 S3 client.

    Returns:
        UploadResponse with upload details.
    """
    client = s3_client or create_s3_client()

    extra_args: dict[str, str | dict] = {
        "ContentType": content_type,
        "StorageClass": storage_class,
    }
    if metadata:
        extra_args["Metadata"] = metadata
    if acl:
        extra_args["ACL"] = acl

    try:
        client.upload_fileobj(
            Fileobj=fileobj,
            Bucket=bucket,
            Key=key,
            ExtraArgs=extra_args,  # type: ignore[arg-type]
        )
    except ClientError as exc:
        logger.error("S3 upload_fileobj failed for s3://%s/%s: %s", bucket, key, exc)
        raise

    # Retrieve metadata with a HEAD request after upload
    head = client.head_object(Bucket=bucket, Key=key)
    content_length = head.get("ContentLength", 0)
    etag = head.get("ETag", "").strip('"')

    return UploadResponse(
        bucket=bucket,
        key=key,
        etag=etag,
        s3_uri=build_s3_uri(bucket, key),
        content_length=content_length,
    )
