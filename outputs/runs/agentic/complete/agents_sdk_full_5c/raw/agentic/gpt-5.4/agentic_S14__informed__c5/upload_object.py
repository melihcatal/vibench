from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, read_bytes
from storage_models import UploadRequest, UploadResult


def upload_object(request: UploadRequest, region_name: Optional[str] = None) -> UploadResult:
    s3 = get_s3_client(region_name=region_name)
    body = read_bytes(file_path=request.file_path, data=request.data)

    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata

    response = s3.put_object(Bucket=request.bucket, Key=request.key, Body=body, **extra_args)
    return UploadResult(
        bucket=request.bucket,
        key=request.key,
        etag=(response.get("ETag") or "").strip('"') or None,
        version_id=response.get("VersionId"),
        storage_class=response.get("ServerSideEncryption") or response.get("Expiration"),
        size=len(body),
    )
