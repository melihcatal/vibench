from __future__ import annotations

import base64
import hashlib
from typing import Optional

from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResult, coerce_metadata


def upload_object(request: UploadObjectRequest) -> UploadObjectResult:
    if not request.file_path and request.data is None:
        raise ValueError("file_path or data is required")

    s3 = get_s3_client("s3")
    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    metadata = coerce_metadata(request.metadata)
    if metadata:
        extra_args["Metadata"] = metadata

    if request.file_path:
        with open(request.file_path, "rb") as infile:
            payload = infile.read()
    else:
        payload = request.data or b""

    checksum_sha256 = base64.b64encode(hashlib.sha256(payload).digest()).decode("ascii")
    extra_args["ChecksumSHA256"] = checksum_sha256

    response = s3.put_object(
        Bucket=request.bucket, Key=request.key, Body=payload, **extra_args
    )
    return UploadObjectResult(
        bucket=request.bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        checksum_sha256=checksum_sha256,
    )


def upload_bytes(
    bucket: str,
    key: str,
    data: bytes,
    content_type: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> UploadObjectResult:
    return upload_object(
        UploadObjectRequest(
            bucket=bucket,
            key=key,
            data=data,
            content_type=content_type,
            metadata=metadata,
        )
    )
