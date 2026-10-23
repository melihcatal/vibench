from __future__ import annotations

from storage_client import get_s3_client
from storage_models import (
    PresignedDownloadRequest,
    PresignedDownloadResult,
    utc_expiration,
)


def create_presigned_download(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResult:
    s3 = get_s3_client()
    params: dict[str, str] = {"Bucket": request.bucket, "Key": request.key}
    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=request.expires_in_seconds,
    )
    return PresignedDownloadResult(
        bucket=request.bucket,
        key=request.key,
        url=url,
        expires_at=utc_expiration(request.expires_in_seconds),
    )
