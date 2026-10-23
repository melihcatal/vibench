from typing import Any, Optional

from storage_client import storage_client
from storage_models import (
    UploadRequest,
    UploadResponse,
    normalize_bytes,
    normalize_metadata,
)


def upload_object(
    bucket: str,
    object_name: str,
    body: Any,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> UploadResponse:
    request = UploadRequest(
        bucket=bucket,
        object_name=object_name,
        body=body,
        content_type=content_type,
        metadata=metadata or {},
    )
    client = storage_client("s3")
    kwargs = {
        "Bucket": request.bucket,
        "Key": request.object_name,
        "Body": normalize_bytes(request.body),
        "Metadata": normalize_metadata(request.metadata),
    }
    if request.content_type:
        kwargs["ContentType"] = request.content_type
    result = client.put_object(**kwargs)
    return UploadResponse(
        bucket=request.bucket,
        object_name=request.object_name,
        etag=result.get("ETag"),
        version_id=result.get("VersionId"),
        raw=result,
    )
