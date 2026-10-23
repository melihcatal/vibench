"""
upload_object.py - Uploads a file or byte stream to managed object storage.

Uses Amazon S3 via boto3 as the concrete managed object storage provider.
Authentication via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
"""

import os
from typing import Optional, BinaryIO

from botocore.exceptions import ClientError

from storage_client import get_s3_client, validate_bucket_exists
from storage_models import StorageUploadRequest, StorageUploadResponse


def upload_object(
    request: StorageUploadRequest,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> StorageUploadResponse:
    """
    Upload a file or byte stream to Amazon S3.

    Args:
        request: StorageUploadRequest containing bucket, key, content, and options.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        StorageUploadResponse with upload result details.

    Raises:
        ValueError: If neither content nor file_path is provided.
        RuntimeError: If the upload fails.
    """
    if request.content is None and request.file_path is None:
        raise ValueError("Either 'content' or 'file_path' must be provided in the upload request.")

    s3_client = get_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    if not validate_bucket_exists(s3_client, request.bucket_name):
        raise RuntimeError(f"Bucket '{request.bucket_name}' does not exist or is not accessible.")

    extra_args = {}

    if request.content_type:
        extra_args["ContentType"] = request.content_type

    if request.metadata:
        extra_args["Metadata"] = request.metadata

    if request.tags:
        tag_string = "&".join(f"{k}={v}" for k, v in request.tags.items())
        extra_args["Tagging"] = tag_string

    if request.storage_class:
        extra_args["StorageClass"] = request.storage_class

    try:
        if request.content is not None:
            response = s3_client.put_object(
                Bucket=request.bucket_name,
                Key=request.object_key,
                Body=request.content,
                **extra_args,
            )
        else:
            with open(request.file_path, "rb") as file_obj:
                response = s3_client.upload_fileobj(
                    Fileobj=file_obj,
                    Bucket=request.bucket_name,
                    Key=request.object_key,
                    ExtraArgs=extra_args,
                )
            response = s3_client.head_object(
                Bucket=request.bucket_name,
                Key=request.object_key,
            )

        return StorageUploadResponse(
            success=True,
            bucket_name=request.bucket_name,
            object_key=request.object_key,
            version_id=response.get("VersionId"),
            etag=response.get("ETag", "").strip('"'),
            request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        raise RuntimeError(
            f"Failed to upload object to S3: {error_code} - {e}"
        ) from e


def upload_bytes(
    bucket_name: str,
    object_key: str,
    data: bytes,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> StorageUploadResponse:
    """
    Convenience function to upload raw bytes to Amazon S3.

    Args:
        bucket_name: Target S3 bucket name.
        object_key: Target S3 object key.
        data: Bytes to upload.
        content_type: Optional MIME content type.
        metadata: Optional user-defined metadata key-value pairs.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        StorageUploadResponse with upload result details.
    """
    request = StorageUploadRequest(
        bucket_name=bucket_name,
        object_key=object_key,
        content=data,
        content_type=content_type,
        metadata=metadata or {},
    )
    return upload_object(
        request,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )


def upload_file(
    bucket_name: str,
    object_key: str,
    file_path: str,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> StorageUploadResponse:
    """
    Convenience function to upload a local file to Amazon S3.

    Args:
        bucket_name: Target S3 bucket name.
        object_key: Target S3 object key.
        file_path: Path to local file to upload.
        content_type: Optional MIME content type.
        metadata: Optional user-defined metadata key-value pairs.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        StorageUploadResponse with upload result details.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Local file not found: {file_path}")

    request = StorageUploadRequest(
        bucket_name=bucket_name,
        object_key=object_key,
        file_path=file_path,
        content_type=content_type,
        metadata=metadata or {},
    )
    return upload_object(
        request,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )
