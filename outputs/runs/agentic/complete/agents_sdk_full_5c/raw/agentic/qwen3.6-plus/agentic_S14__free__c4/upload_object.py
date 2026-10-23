"""Upload a file or byte stream to AWS S3 Managed Object Storage."""

import os
from typing import BinaryIO, Optional, Dict

from storage_client import S3ClientFactory
from storage_models import UploadRequest, UploadResponse


def upload_object(
    key: str,
    content: bytes,
    bucket: Optional[str] = None,
    content_type: str = "application/octet-stream",
    metadata: Optional[Dict[str, str]] = None,
    storage_class: str = "STANDARD",
    server_side_encryption: Optional[str] = "aws:kms",
) -> UploadResponse:
    """
    Upload a file or byte stream to an S3 bucket.

    Uses the AWS SDK for Python (boto3) to call the S3 PutObject API
    against the configured S3 bucket (s3.us-east-1.amazonaws.com or
    custom S3_ENDPOINT_URL).

    Args:
        key: The object key (path) within the bucket.
        content: The raw bytes to upload.
        bucket: Target S3 bucket name (falls back to S3_BUCKET_NAME env var).
        content_type: MIME type of the content.
        metadata: Custom user metadata key-value pairs.
        storage_class: S3 storage class (STANDARD, INTELLIGENT_TIERING, etc.).
        server_side_encryption: SSE type (aws:kms, AES256, or None).

    Returns:
        UploadResponse with ETag, version ID, and content length.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket

    request = UploadRequest(
        bucket=target_bucket,
        key=key,
        content=content,
        content_type=content_type,
        metadata=metadata or {},
        storage_class=storage_class,
        server_side_encryption=server_side_encryption,
    )

    s3_client = factory.s3_client

    response = s3_client.put_object(**request.to_boto_kwargs())

    return UploadResponse.from_boto_response(
        key=key,
        bucket=target_bucket,
        response=response,
        content=content,
    )


def upload_file_stream(
    key: str,
    file_path: str,
    bucket: Optional[str] = None,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    chunk_size: int = 10 * 1024 * 1024,
) -> UploadResponse:
    """
    Upload a file from disk to S3 using boto3's upload_fileobj for streaming.

    Automatically uses S3 Transfer Manager for multipart uploads when the file
    exceeds the multipart threshold on s3.amazonaws.com.

    Args:
        key: The object key within the bucket.
        file_path: Local filesystem path to the file.
        bucket: Target S3 bucket name.
        content_type: MIME type (auto-detected by boto3 if None).
        metadata: Custom metadata dictionary.
        chunk_size: Ignored; boto3 handles multipart thresholds internally.

    Returns:
        UploadResponse with ETag and version ID.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket

    s3_client = factory.s3_client

    extra_args: Dict = {}
    if content_type:
        extra_args["ContentType"] = content_type
    if metadata:
        extra_args["Metadata"] = metadata
    extra_args["ServerSideEncryption"] = "aws:kms"

    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        s3_client.upload_fileobj(
            Fileobj=f,
            Bucket=target_bucket,
            Key=key,
            ExtraArgs=extra_args,
        )

    head = s3_client.head_object(Bucket=target_bucket, Key=key)

    with open(file_path, "rb") as f:
        raw_content = f.read()

    return UploadResponse(
        object_key=key,
        bucket=target_bucket,
        etag=head.get("ETag", "").strip('"'),
        version_id=head.get("VersionId"),
        content_length=file_size,
        storage_class=head.get("StorageClass", "STANDARD"),
    )
