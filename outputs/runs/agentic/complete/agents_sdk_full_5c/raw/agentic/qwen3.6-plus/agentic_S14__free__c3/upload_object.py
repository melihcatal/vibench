"""
Upload a file or byte stream to managed object storage (AWS S3).

Provider: AWS S3 via boto3
- Uses boto3.client('s3') for AWS S3 put_object / upload_file
- AWS S3 endpoint: https://s3.{region}.amazonaws.com
"""

import os
import logging
from typing import IO, Optional, Dict

from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResponse, normalize_upload_response

logger = logging.getLogger(__name__)


def upload_object(
    bucket: str,
    key: str,
    body: Optional[bytes] = None,
    file_path: Optional[str] = None,
    file_obj: Optional[IO[bytes]] = None,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    storage_class: Optional[str] = None,
) -> UploadResponse:
    """
    Upload an object to AWS S3.

    Supports uploading from bytes, a file path, or a file-like object.

    Provider signals:
    - boto3 S3 client (AWS S3 managed object storage)
    - put_object / upload_fileobj S3 APIs
    - AWS S3 storage classes (STANDARD, INTELLIGENT_TIERING, etc.)
    """
    s3_client = get_s3_client()

    request = UploadRequest(
        bucket=bucket,
        key=key,
        body=body,
        file_path=file_path,
        content_type=content_type,
        metadata=metadata or {},
        storage_class=storage_class,
    )

    upload_kwargs: Dict = {
        "Bucket": bucket,
        "Key": key,
    }

    if content_type:
        upload_kwargs["ContentType"] = content_type
    if metadata:
        upload_kwargs["Metadata"] = metadata
    if storage_class:
        upload_kwargs["StorageClass"] = storage_class

    if file_path and os.path.isfile(file_path):
        logger.info("Uploading file %s to s3://%s/%s", file_path, bucket, key)
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type
        if metadata:
            extra_args["Metadata"] = metadata
        if storage_class:
            extra_args["StorageClass"] = storage_class
        raw = s3_client.upload_file(
            Filename=file_path,
            Bucket=bucket,
            Key=key,
            ExtraArgs=extra_args,
        )
        head = s3_client.head_object(Bucket=bucket, Key=key)
        return normalize_upload_response(head, bucket, key)

    resolved_body = request.resolve_body() if body is not None else None

    if file_obj is not None:
        logger.info("Uploading file object to s3://%s/%s", bucket, key)
        raw = s3_client.upload_fileobj(
            Fileobj=file_obj,
            Bucket=bucket,
            Key=key,
            ExtraArgs=upload_kwargs,
        )
        head = s3_client.head_object(Bucket=bucket, Key=key)
        return normalize_upload_response(head, bucket, key)

    if resolved_body is None:
        raise ValueError("Must provide body, file_path, or file_obj for upload")

    upload_kwargs["Body"] = resolved_body

    logger.info("Uploading %d bytes to s3://%s/%s", len(resolved_body), bucket, key)
    raw = s3_client.put_object(**upload_kwargs)

    return normalize_upload_response(raw, bucket, key)
