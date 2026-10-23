from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResult


def upload_object(request: UploadRequest) -> UploadResult:
    s3 = get_s3_client()
    extra_args: dict[str, object] = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata

    if request.file_path:
        with Path(request.file_path).open("rb") as file_obj:
            response = s3.put_object(
                Bucket=request.bucket,
                Key=request.key,
                Body=file_obj,
                **extra_args,
            )
    elif request.data is not None:
        response = s3.put_object(
            Bucket=request.bucket,
            Key=request.key,
            Body=request.data,
            **extra_args,
        )
    else:
        raise ValueError("Either file_path or data must be provided")

    return UploadResult(
        bucket=request.bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
    )


def upload_stream(bucket: str, key: str, stream: BinaryIO, content_type: str | None = None) -> UploadResult:
    s3 = get_s3_client()
    params: dict[str, object] = {"Bucket": bucket, "Key": key, "Body": stream}
    if content_type:
        params["ContentType"] = content_type
    response = s3.put_object(**params)
    return UploadResult(bucket=bucket, key=key, etag=response.get("ETag"), version_id=response.get("VersionId"))
