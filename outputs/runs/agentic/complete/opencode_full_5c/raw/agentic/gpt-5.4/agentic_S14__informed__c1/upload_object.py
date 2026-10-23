from __future__ import annotations

from typing import BinaryIO

from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResult, normalize_metadata


def upload_object(request: UploadObjectRequest) -> UploadObjectResult:
    if not request.file_path and request.data is None:
        raise ValueError("file_path or data is required")
    client = get_s3_client()
    extra_args: dict[str, object] = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    metadata = normalize_metadata(request.metadata)
    if metadata:
        extra_args["Metadata"] = metadata
    if request.file_path:
        with open(request.file_path, "rb") as file_obj:
            return _upload_fileobj(client, file_obj, request, extra_args)
    return _put_bytes(client, request, extra_args)


def _upload_fileobj(
    client,
    file_obj: BinaryIO,
    request: UploadObjectRequest,
    extra_args: dict[str, object],
) -> UploadObjectResult:
    response = client.upload_fileobj(
        file_obj, request.bucket, request.key, ExtraArgs=extra_args or None
    )
    head = client.head_object(Bucket=request.bucket, Key=request.key)
    return UploadObjectResult(
        bucket=request.bucket,
        key=request.key,
        etag=head.get("ETag"),
        version_id=head.get("VersionId"),
        size=head.get("ContentLength"),
    )


def _put_bytes(
    client, request: UploadObjectRequest, extra_args: dict[str, object]
) -> UploadObjectResult:
    body = request.data if request.data is not None else b""
    params = {"Bucket": request.bucket, "Key": request.key, "Body": body, **extra_args}
    response = client.put_object(**params)
    return UploadObjectResult(
        bucket=request.bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        size=len(body),
    )
