from __future__ import annotations

from typing import BinaryIO

from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResult


def upload_object(request: UploadObjectRequest) -> UploadObjectResult:
    s3 = get_s3_client()
    extra_args: dict[str, object] = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata
    if request.file_path:
        s3.upload_file(
            request.file_path,
            request.bucket,
            request.object_name,
            ExtraArgs=extra_args or None,
        )
        head = s3.head_object(Bucket=request.bucket, Key=request.object_name)
        return UploadObjectResult(
            bucket=request.bucket,
            object_name=request.object_name,
            etag=head.get("ETag"),
            version_id=head.get("VersionId"),
            content_type=head.get("ContentType"),
            size=head.get("ContentLength"),
        )
    body: bytes | BinaryIO
    if request.data is None:
        raise ValueError("request.data or request.file_path is required")
    body = request.data
    response = s3.put_object(
        Bucket=request.bucket, Key=request.object_name, Body=body, **extra_args
    )
    head = s3.head_object(Bucket=request.bucket, Key=request.object_name)
    return UploadObjectResult(
        bucket=request.bucket,
        object_name=request.object_name,
        etag=response.get("ETag") or head.get("ETag"),
        version_id=response.get("VersionId") or head.get("VersionId"),
        content_type=head.get("ContentType"),
        size=head.get("ContentLength"),
    )
