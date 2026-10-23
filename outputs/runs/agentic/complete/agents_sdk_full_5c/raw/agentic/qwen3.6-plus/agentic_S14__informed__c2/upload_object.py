"""
upload_object.py - Upload a file or byte stream to Amazon S3 managed object storage.

Uses the boto3 SDK (Amazon S3).
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""
from __future__ import annotations

import os
from typing import Optional

from botocore.exceptions import ClientError

from storage_client import create_s3_client, read_file_as_bytes, bytes_to_fileobj, get_content_type, handle_s3_error
from storage_models import StorageUploadRequest, StorageUploadResponse, build_s3_metadata


def upload_object(
    bucket: str,
    key: str,
    file_path: Optional[str] = None,
    data: Optional[bytes] = None,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
    storage_class: str = "STANDARD",
    acl: str = "private",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> StorageUploadResponse:
    """
    Upload a file or raw bytes to an Amazon S3 bucket.

    Args:
        bucket: S3 bucket name.
        key: Object key (path) within the bucket.
        file_path: Local filesystem path to the file to upload.
        data: Raw bytes to upload (alternative to file_path).
        content_type: MIME type of the uploaded object.
        metadata: Custom user-defined metadata key-value pairs.
        storage_class: S3 storage class (STANDARD, INTELLIGENT_TIERING, GLACIER, etc.)
        acl: Access control list (private, public-read, bucket-owner-full-control, etc.)
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.
        endpoint_url: Optional S3 endpoint URL override.

    Returns:
        StorageUploadResponse with success status and S3 metadata.
    """
    request = StorageUploadRequest(
        bucket=bucket,
        key=key,
        file_path=file_path,
        data=data,
        content_type=content_type,
        metadata=metadata or {},
        storage_class=storage_class,
        acl=acl,
    )

    client = create_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region=region,
        endpoint_url=endpoint_url,
    )

    try:
        upload_kwargs = {
            "Bucket": request.bucket,
            "Key": request.key,
            "StorageClass": request.storage_class,
            "ACL": request.acl,
        }

        # Prepare body
        if request.file_path:
            upload_body = read_file_as_bytes(request.file_path)
            if not request.content_type:
                upload_kwargs["ContentType"] = get_content_type(request.file_path)
        elif request.data:
            upload_body = request.data
        else:
            return StorageUploadResponse(
                success=False,
                bucket=request.bucket,
                key=request.key,
                error="Either file_path or data must be provided",
            )

        if request.content_type:
            upload_kwargs["ContentType"] = request.content_type

        # Metadata
        if request.metadata:
            upload_kwargs["Metadata"] = build_s3_metadata(request.metadata)

        # Execute upload using S3 put_object via boto3
        response = client.put_object(Body=upload_body, **upload_kwargs)

        return StorageUploadResponse(
            success=True,
            bucket=request.bucket,
            key=request.key,
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
            storage_class=response.get("StorageClass", request.storage_class),
        )

    except ClientError as e:
        return StorageUploadResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error=handle_s3_error(e, "upload_object"),
        )
