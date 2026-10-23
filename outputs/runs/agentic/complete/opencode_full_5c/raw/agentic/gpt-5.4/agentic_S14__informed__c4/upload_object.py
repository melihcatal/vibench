from __future__ import annotations

from typing import BinaryIO, Optional, Union

from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResult


def upload_object(
    request: UploadObjectRequest,
    stream: Optional[BinaryIO] = None,
) -> UploadObjectResult:
    s3 = get_s3_client()
    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata
    if request.file_path:
        s3.upload_file(
            request.file_path, request.bucket, request.key, ExtraArgs=extra_args or None
        )
    else:
        body: Union[bytes, BinaryIO]
        if stream is not None:
            body = stream
        elif request.data is not None:
            body = request.data
        else:
            raise ValueError("file_path, data, or stream is required")
        s3.put_object(Bucket=request.bucket, Key=request.key, Body=body, **extra_args)
    head = s3.head_object(Bucket=request.bucket, Key=request.key)
    return UploadObjectResult(
        bucket=request.bucket,
        key=request.key,
        etag=(head.get("ETag") or "").strip('"') or None,
        version_id=head.get("VersionId"),
    )
