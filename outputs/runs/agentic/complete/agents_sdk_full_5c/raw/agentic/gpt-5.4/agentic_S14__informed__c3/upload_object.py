from __future__ import annotations

from typing import Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import UploadRequest, UploadResult


def upload_object(request: UploadRequest, region_name: Optional[str] = None) -> UploadResult:
    s3 = get_s3_client(region_name=region_name)
    bucket = get_bucket_name(request.bucket)

    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata

    if request.file_path:
        s3.upload_file(request.file_path, bucket, request.key, ExtraArgs=extra_args or None)
        head = s3.head_object(Bucket=bucket, Key=request.key)
        return UploadResult(
            bucket=bucket,
            key=request.key,
            etag=(head.get("ETag") or "").strip('"') or None,
            version_id=head.get("VersionId"),
        )

    if request.data is None:
        raise ValueError("Either file_path or data must be provided.")

    response = s3.put_object(Bucket=bucket, Key=request.key, Body=request.data, **extra_args)
    return UploadResult(
        bucket=bucket,
        key=request.key,
        etag=(response.get("ETag") or "").strip('"') or None,
        version_id=response.get("VersionId"),
    )
