"""
Upload a file or byte stream to Amazon S3 Managed Object Storage.

Uses boto3 SDK for Amazon S3 (service=Amazon S3).
Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

import io
from typing import Any, Dict, Optional

from storage_client import get_s3_client, validate_bucket_name, build_object_key
from storage_models import UploadRequest, UploadResponse


def upload_object(
    bucket: str,
    object_key: str,
    body: Any,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    storage_class: str = "STANDARD",
    prefix: Optional[str] = None,
) -> UploadResponse:
    """
    Upload a file or byte stream to Amazon S3.

    Args:
        bucket: The S3 bucket name.
        object_key: The object key (filename or path within the bucket).
        body: The file content as bytes or a file-like object.
        content_type: Optional MIME type; auto-detected if not provided.
        metadata: Optional user-defined metadata key-value pairs.
        storage_class: S3 storage class (e.g., STANDARD, INTELLIGENT_TIERING, GLACIER).
        prefix: Optional prefix to prepend to the object key.

    Returns:
        UploadResponse with etag, version_id, and upload details.

    Raises:
        ValueError: If bucket name is invalid or body is empty.
        ClientError: On S3 API errors (e.g., NoSuchBucket, AccessDenied).
    """
    validate_bucket_name(bucket)

    if prefix:
        object_key = build_object_key(prefix, object_key)

    # Convert body to bytes or file-like object
    if isinstance(body, str):
        body = body.encode("utf-8")

    if isinstance(body, bytes):
        body = io.BytesIO(body)

    if hasattr(body, "seek"):
        body.seek(0)
        body_bytes = body.read()
        body = io.BytesIO(body_bytes)
        content_length = len(body_bytes)
    else:
        content_length = None

    request = UploadRequest(
        bucket=bucket,
        object_key=object_key,
        body=body,
        content_type=content_type,
        content_length=content_length,
        metadata=metadata or {},
        storage_class=storage_class,
    )

    detected_content_type = request.detect_content_type()

    put_kwargs = {
        "Bucket": bucket,
        "Key": object_key,
        "Body": body,
        "ContentType": detected_content_type,
        "StorageClass": storage_class,
    }

    if request.metadata:
        put_kwargs["Metadata"] = request.metadata

    s3_client = get_s3_client()
    response = s3_client.put_object(**put_kwargs)

    return UploadResponse.from_s3_response(response, request)


def upload_file(
    bucket: str,
    file_path: str,
    object_key: Optional[str] = None,
    prefix: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    storage_class: str = "STANDARD",
) -> UploadResponse:
    """
    Upload a local file to Amazon S3.

    Args:
        bucket: The S3 bucket name.
        file_path: Local filesystem path to the file.
        object_key: Optional S3 object key; defaults to the filename.
        prefix: Optional prefix to prepend to the object key.
        metadata: Optional user-defined metadata.
        storage_class: S3 storage class.

    Returns:
        UploadResponse with upload details.
    """
    import os

    if object_key is None:
        object_key = os.path.basename(file_path)

    if prefix:
        object_key = build_object_key(prefix, object_key)

    content_type, _ = None, None  # auto-detect in upload_object

    with open(file_path, "rb") as f:
        body = f.read()

    return upload_object(
        bucket=bucket,
        object_key=object_key,
        body=body,
        content_type=content_type,
        metadata=metadata,
        storage_class=storage_class,
    )
