from __future__ import annotations

from storage_client import get_s3_client, read_upload_bytes
from storage_models import (
    UploadObjectRequest,
    UploadObjectResult,
    normalize_metadata_map,
    s3_uri,
)


def upload_object(request: UploadObjectRequest) -> UploadObjectResult:
    s3 = get_s3_client()
    payload = read_upload_bytes(request.body, request.file_path)
    params: dict[str, object] = {
        "Bucket": request.bucket,
        "Key": request.key,
        "Body": payload,
    }
    if request.content_type:
        params["ContentType"] = request.content_type
    metadata = normalize_metadata_map(request.metadata)
    if metadata:
        params["Metadata"] = metadata
    response = s3.put_object(**params)
    return UploadObjectResult(
        bucket=request.bucket,
        key=request.key,
        etag=response.get("ETag"),
        version_id=response.get("VersionId"),
        uri=s3_uri(request.bucket, request.key),
    )
