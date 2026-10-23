from __future__ import annotations

from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResult


def create_presigned_download(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResult:
    client = get_s3_client()
    params = {"Bucket": request.bucket, "Key": request.key}
    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type
    url = client.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=request.expires_in,
    )
    return PresignedDownloadResult(
        bucket=request.bucket,
        key=request.key,
        url=url,
        expires_in=request.expires_in,
    )
