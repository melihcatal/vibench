from __future__ import annotations

from storage_client import get_s3_bucket, get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    if request.file_path is None and request.data is None:
        raise ValueError("Either file_path or data must be provided")
    client = get_s3_client()
    bucket = get_s3_bucket(request.bucket)
    extra_args: dict[str, object] = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata
    if request.file_path:
        client.upload_file(
            request.file_path, bucket, request.object_key, ExtraArgs=extra_args or None
        )
        head = client.head_object(Bucket=bucket, Key=request.object_key)
        return UploadObjectResponse(
            bucket=bucket,
            object_key=request.object_key,
            etag=head.get("ETag"),
            version_id=head.get("VersionId"),
            checksum_sha256=head.get("ChecksumSHA256"),
        )
    response = client.put_object(
        Bucket=bucket, Key=request.object_key, Body=request.data, **extra_args
    )
    return UploadObjectResponse(
        bucket=bucket,
        object_key=request.object_key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        checksum_sha256=response.get("ChecksumSHA256"),
    )
