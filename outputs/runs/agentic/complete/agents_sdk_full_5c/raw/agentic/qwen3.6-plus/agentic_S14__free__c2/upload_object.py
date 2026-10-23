"""
Upload a file or byte stream to managed object storage (AWS S3).

Uses boto3 S3 client to upload objects with configurable metadata and options.
"""

import os
from typing import Optional, BinaryIO, Dict, Any

from storage_client import get_s3_client, get_bucket_name, validate_object_key
from storage_models import (
    UploadRequest,
    UploadResponse,
    detect_content_type,
    prepare_upload_body,
)


def upload_object(
    key: str,
    content: Optional[bytes] = None,
    file_path: Optional[str] = None,
    stream: Optional[BinaryIO] = None,
    bucket: Optional[str] = None,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    cache_control: Optional[str] = None,
    storage_class: Optional[str] = None,
    encryption: Optional[str] = "AES256",
    acl: Optional[str] = None,
    s3_client=None,
) -> UploadResponse:
    """
    Upload a file or byte stream to an S3 bucket.

    Args:
        key: S3 object key (path within the bucket)
        content: Raw bytes to upload
        file_path: Path to local file to upload
        stream: Binary stream to upload
        bucket: Target S3 bucket name
        content_type: MIME type of the content
        metadata: User-defined metadata key-value pairs
        cache_control: Cache-Control header value
        storage_class: S3 storage class (STANDARD, GLACIER, etc.)
        encryption: Server-side encryption type
        acl: Access control list setting
        s3_client: Pre-configured boto3 S3 client

    Returns:
        UploadResponse with upload result details
    """
    validate_object_key(key)
    bucket_name = get_bucket_name(bucket)
    client = s3_client or get_s3_client()

    upload_req = UploadRequest(
        bucket=bucket_name,
        key=key,
        content_type=content_type,
        metadata=metadata,
        cache_control=cache_control,
        storage_class=storage_class,
        encryption=encryption,
        acl=acl,
    )

    try:
        upload_body = prepare_upload_body(content=content, file_path=file_path, stream=stream)
        data_bytes = content if content is not None else None

        if data_bytes is None and hasattr(upload_body, "read"):
            data_bytes = upload_body.read()
            upload_body.seek(0)

        detected_content_type = upload_req.content_type or detect_content_type(key, data_bytes)

        put_params: Dict[str, Any] = {
            "Bucket": upload_req.bucket,
            "Key": upload_req.key,
            "ContentType": detected_content_type,
        }

        if upload_body is not None:
            put_params["Body"] = upload_body

        if upload_req.metadata:
            put_params["Metadata"] = upload_req.metadata
        if upload_req.cache_control:
            put_params["CacheControl"] = upload_req.cache_control
        if upload_req.storage_class:
            put_params["StorageClass"] = upload_req.storage_class
        if upload_req.encryption:
            put_params["ServerSideEncryption"] = upload_req.encryption
        if upload_req.acl:
            put_params["ACL"] = upload_req.acl

        response = client.put_object(**put_params)

        upload_response = UploadResponse.from_s3_response(
            bucket=upload_req.bucket,
            key=upload_req.key,
            s3_response=response,
            success=True,
        )
        upload_response.content_length = len(data_bytes) if data_bytes else 0
        upload_response.content_type = detected_content_type

        return upload_response

    except client.exceptions.ClientError as e:
        return UploadResponse(
            bucket=bucket_name,
            key=key,
            etag="",
            success=False,
            error_message=str(e),
        )
    finally:
        if upload_body is not None and hasattr(upload_body, "close"):
            upload_body.close()


def upload_from_local_file(file_path: str, key: Optional[str] = None, **kwargs) -> UploadResponse:
    """
    Convenience function to upload a local file to S3.

    Args:
        file_path: Path to the local file
        key: Optional S3 key (defaults to basename of file_path)
        **kwargs: Additional parameters passed to upload_object
    """
    if key is None:
        key = os.path.basename(file_path)
    return upload_object(key=key, file_path=file_path, **kwargs)


def upload_bytes(data: bytes, key: str, **kwargs) -> UploadResponse:
    """
    Convenience function to upload raw bytes to S3.

    Args:
        data: Raw bytes to upload
        key: S3 object key
        **kwargs: Additional parameters passed to upload_object
    """
    return upload_object(key=key, content=data, **kwargs)
