from __future__ import annotations

from typing import Any

from storage_client import create_storage_client
from storage_models import UploadRequest


def upload_object(request: UploadRequest) -> dict[str, Any]:
    s3 = create_storage_client("s3")
    kwargs: dict[str, Any] = {"Bucket": request.bucket, "Key": request.key, "Body": request.body}
    if request.content_type:
        kwargs["ContentType"] = request.content_type
    if request.metadata:
        kwargs["Metadata"] = request.metadata
    kwargs.update(request.extra_args)
    response = s3.put_object(**kwargs)
    return {"bucket": request.bucket, "key": request.key, "etag": response.get("ETag"), "version_id": response.get("VersionId"), "raw": response}
