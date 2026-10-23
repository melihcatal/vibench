from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResult


def upload_object(request: UploadRequest, region_name: Optional[str] = None) -> UploadResult:
    if not request.file_path and request.data is None:
        raise ValueError("Either file_path or data must be provided")

    s3 = get_s3_client(region_name=region_name)
    extra_args: dict[str, object] = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata

    if request.file_path:
        s3.upload_file(request.file_path, request.bucket, request.key, ExtraArgs=extra_args or None)
        head = s3.head_object(Bucket=request.bucket, Key=request.key)
        return UploadResult(
            bucket=request.bucket,
            key=request.key,
            etag=str(head.get("ETag", "")).strip('"') or None,
            version_id=head.get("VersionId"),
            checksum_sha256=head.get("ChecksumSHA256"),
        )

    response = s3.put_object(
        Bucket=request.bucket,
        Key=request.key,
        Body=request.data,
        **extra_args,
    )
    return UploadResult(
        bucket=request.bucket,
        key=request.key,
        etag=str(response.get("ETag", "")).strip('"') or None,
        version_id=response.get("VersionId"),
        checksum_sha256=response.get("ChecksumSHA256"),
    )
