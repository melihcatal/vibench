from __future__ import annotations

from storage_client import get_s3_client, read_binary_payload
from storage_models import UploadObjectRequest, UploadObjectResult, normalize_metadata


def upload_object(request: UploadObjectRequest) -> UploadObjectResult:
    s3_client = get_s3_client()
    body = read_binary_payload(request.data)
    extra_args: dict[str, object] = {}
    if request.content_type:
        extra_args["ContentType"] = request.content_type
    metadata = normalize_metadata(request.metadata)
    if metadata:
        extra_args["Metadata"] = metadata
    s3_client.put_object(
        Bucket=request.bucket_name, Key=request.object_name, Body=body, **extra_args
    )
    head = s3_client.head_object(Bucket=request.bucket_name, Key=request.object_name)
    return UploadObjectResult(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        etag=(head.get("ETag") or "").strip('"') or None,
        version_id=head.get("VersionId"),
        size=head.get("ContentLength"),
        content_type=head.get("ContentType"),
        metadata=normalize_metadata(head.get("Metadata")),
    )
