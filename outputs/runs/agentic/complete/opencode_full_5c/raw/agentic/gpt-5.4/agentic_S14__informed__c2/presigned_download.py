from __future__ import annotations

from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResult


def create_presigned_download(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResult:
    s3_client = get_s3_client()
    params = {"Bucket": request.bucket_name, "Key": request.object_name}
    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type
    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=request.expires_in_seconds,
    )
    return PresignedDownloadResult(
        bucket_name=request.bucket_name,
        object_name=request.object_name,
        url=url,
        expires_in_seconds=request.expires_in_seconds,
    )
