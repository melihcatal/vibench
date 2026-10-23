"""
Upload a file or byte stream to managed object storage.

Uses AWS S3 (boto3) as the concrete managed object storage provider.
Supports uploading raw bytes, file-like objects, or local file paths.
"""

from typing import BinaryIO, Dict, Optional, Union

import boto3
from botocore.exceptions import ClientError

from storage_client import StorageClient, StorageClientConfig, get_client
from storage_models import (
    StorageObjectRequest,
    StorageUploadResponse,
    normalize_metadata,
)


def upload_object(
    bucket: str,
    key: str,
    data: Optional[Union[bytes, BinaryIO]] = None,
    file_path: Optional[str] = None,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    storage_class: Optional[str] = None,
    acl: Optional[str] = None,
    server_side_encryption: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    client: Optional[StorageClient] = None,
) -> StorageUploadResponse:
    """
    Upload a file or byte stream to an AWS S3 bucket.

    Args:
        bucket: S3 bucket name to upload into.
        key: Object key (path) within the bucket.
        data: Raw bytes or file-like object to upload.
        file_path: Local file path to upload from.
        content_type: MIME type of the uploaded content.
        metadata: User-defined metadata key-value pairs.
        storage_class: S3 storage class (STANDARD, GLACIER, etc.).
        acl: Canned ACL for the uploaded object.
        server_side_encryption: SSE algorithm (AES256, aws:kms).
        tags: S3 object tags.
        client: Optional pre-configured StorageClient instance.

    Returns:
        StorageUploadResponse with upload result details.

    Raises:
        ValueError: If neither data nor file_path is provided.
        ClientError: If the S3 upload fails.
    """
    if client is None:
        client = get_client()

    s3_client = client.get_s3_client()

    request = StorageObjectRequest(
        bucket=bucket,
        key=key,
        data=data,
        file_path=file_path,
        content_type=content_type,
        metadata=metadata,
        storage_class=storage_class,
        server_side_encryption=server_side_encryption,
        acl=acl,
        tags=tags,
    )

    content_type = request.resolve_content_type()
    normalized_metadata = normalize_metadata(metadata)

    upload_params = {
        "Bucket": bucket,
        "Key": key,
        "ContentType": content_type,
        "Metadata": normalized_metadata,
    }

    if storage_class:
        upload_params["StorageClass"] = storage_class
    if acl:
        upload_params["ACL"] = acl
    if server_side_encryption:
        upload_params["ServerSideEncryption"] = server_side_encryption
    if tags:
        tag_string = "&".join(f"{k}={v}" for k, v in tags.items())
        upload_params["Tagging"] = tag_string

    try:
        data_stream = request.get_data_stream()
        try:
            if hasattr(data_stream, "seek"):
                data_stream.seek(0)
            response = s3_client.put_object(Body=data_stream, **upload_params)
        finally:
            if hasattr(data_stream, "close") and data_stream != data:
                data_stream.close()

        etag = response.get("ETag", "").strip('"')
        version_id = response.get("VersionId")
        sse = response.get("ServerSideEncryption")
        expiration = response.get("Expiration")

        content_length = 0
        if data is not None and isinstance(data, bytes):
            content_length = len(data)
        elif file_path:
            import os
            content_length = os.path.getsize(file_path)

        from storage_client import format_s3_uri

        return StorageUploadResponse(
            bucket=bucket,
            key=key,
            etag=etag,
            version_id=version_id,
            storage_class=storage_class,
            content_type=content_type,
            content_length=content_length,
            server_side_encryption=sse,
            expiration=expiration,
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
            s3_uri=format_s3_uri(bucket, key),
        )

    except ClientError as e:
        raise ClientError(
            e.response,
            f"Failed to upload object s3://{bucket}/{key}: {e}",
        )


def upload_file_stream(
    bucket: str,
    key: str,
    stream: BinaryIO,
    content_type: Optional[str] = "application/octet-stream",
    metadata: Optional[Dict[str, str]] = None,
    client: Optional[StorageClient] = None,
) -> StorageUploadResponse:
    """
    Upload a file-like stream object to S3.

    Args:
        bucket: S3 bucket name.
        key: Object key within the bucket.
        stream: File-like object with read() method.
        content_type: MIME type.
        metadata: User metadata.
        client: Optional StorageClient.

    Returns:
        StorageUploadResponse with upload details.
    """
    return upload_object(
        bucket=bucket,
        key=key,
        data=stream,
        content_type=content_type,
        metadata=metadata,
        client=client,
    )


def upload_bytes(
    bucket: str,
    key: str,
    data: bytes,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    client: Optional[StorageClient] = None,
) -> StorageUploadResponse:
    """
    Upload raw bytes directly to S3.

    Args:
        bucket: S3 bucket name.
        key: Object key within the bucket.
        data: Raw bytes to upload.
        content_type: MIME type.
        metadata: User metadata.
        client: Optional StorageClient.

    Returns:
        StorageUploadResponse with upload details.
    """
    return upload_object(
        bucket=bucket,
        key=key,
        data=data,
        content_type=content_type,
        metadata=metadata,
        client=client,
    )
