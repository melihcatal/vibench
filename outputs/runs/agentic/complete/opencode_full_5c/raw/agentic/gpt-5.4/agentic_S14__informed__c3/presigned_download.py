from __future__ import annotations

from storage_client import get_s3_client
from storage_models import PresignedDownloadRequest


def create_presigned_download_url(request: PresignedDownloadRequest) -> str:
    s3 = get_s3_client()
    params = {"Bucket": request.bucket, "Key": request.key}
    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=request.expires_in_seconds,
    )
