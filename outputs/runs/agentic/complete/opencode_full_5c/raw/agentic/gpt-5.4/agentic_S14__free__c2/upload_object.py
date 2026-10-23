from __future__ import annotations

from typing import Union

from storage_client import build_s3_client, build_s3_uri, require_bucket
from storage_models import UploadObjectRequest, UploadObjectResult


def upload_object(request: UploadObjectRequest) -> UploadObjectResult:
    s3 = build_s3_client()
    bucket = require_bucket(request.bucket)
    body: Union[bytes, str] = request.body
    response = s3.put_object(
        Bucket=bucket,
        Key=request.key,
        Body=body,
        ContentType=request.content_type or "application/octet-stream",
        Metadata=request.metadata or {},
    )
    return UploadObjectResult(
        bucket=bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        checksum=response.get("ChecksumSHA256") or response.get("ChecksumCRC32"),
        url=build_s3_uri(bucket, request.key),
    )
