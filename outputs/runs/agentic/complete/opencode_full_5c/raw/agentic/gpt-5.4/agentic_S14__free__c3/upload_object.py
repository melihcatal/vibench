from __future__ import annotations

from storage_client import get_s3_client
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(request: UploadObjectRequest) -> UploadObjectResponse:
    s3 = get_s3_client()
    extra_args: dict[str, object] = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    if request.metadata:
        extra_args["Metadata"] = request.metadata

    if request.file_path:
        s3.upload_file(
            request.file_path, request.bucket, request.key, ExtraArgs=extra_args or None
        )
        head = s3.head_object(Bucket=request.bucket, Key=request.key)
        return UploadObjectResponse(
            bucket=request.bucket,
            key=request.key,
            etag=head.get("ETag"),
            version_id=head.get("VersionId"),
        )

    if request.data is None:
        raise ValueError("Either file_path or data must be provided")

    response = s3.put_object(
        Bucket=request.bucket, Key=request.key, Body=request.data, **extra_args
    )
    return UploadObjectResponse(
        bucket=request.bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
    )
