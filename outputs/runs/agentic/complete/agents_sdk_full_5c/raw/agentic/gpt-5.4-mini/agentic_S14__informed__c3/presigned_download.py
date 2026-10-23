from __future__ import annotations

from typing import Any

from storage_client import create_storage_client
from storage_models import PresignedUrlRequest


def create_presigned_download_url(request: PresignedUrlRequest) -> dict[str, Any]:
    s3 = create_storage_client("s3")
    params: dict[str, Any] = {"Bucket": request.bucket, "Key": request.key}
    if request.version_id:
        params["VersionId"] = request.version_id
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=request.expires_in,
    )
    return {"bucket": request.bucket, "key": request.key, "expires_in": request.expires_in, "url": url}
