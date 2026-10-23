from __future__ import annotations

from typing import Optional

from storage_client import get_default_bucket, get_s3_client
from storage_models import UploadRequest, UploadResult, s3_uri


def upload_object(request: UploadRequest, region: Optional[str] = None) -> UploadResult:
    if not request.file_path and request.data is None:
        raise ValueError("Either file_path or data must be provided.")

    bucket = get_default_bucket(request.bucket)
    s3 = get_s3_client(region=region)

    extra_args = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata

    if request.file_path:
        s3.upload_file(request.file_path, bucket, request.key, ExtraArgs=extra_args or None)
        head = s3.head_object(Bucket=bucket, Key=request.key)
    else:
        put_response = s3.put_object(Bucket=bucket, Key=request.key, Body=request.data, **extra_args)
        head = s3.head_object(Bucket=bucket, Key=request.key)
        if "ETag" not in head and "ETag" in put_response:
            head["ETag"] = put_response["ETag"]

    return UploadResult(
        bucket=bucket,
        key=request.key,
        etag=head.get("ETag"),
        version_id=head.get("VersionId"),
        checksum_sha256=head.get("ChecksumSHA256"),
        uri=s3_uri(bucket, request.key),
    )
