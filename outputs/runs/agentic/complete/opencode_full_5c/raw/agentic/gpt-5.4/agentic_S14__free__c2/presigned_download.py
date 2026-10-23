from __future__ import annotations

from storage_client import build_s3_client, require_bucket
from storage_models import PresignedDownloadRequest


def create_presigned_download_url(request: PresignedDownloadRequest) -> str:
    s3 = build_s3_client()
    bucket = require_bucket(request.bucket)
    params = {"Bucket": bucket, "Key": request.key}
    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type
    return s3.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=request.expires_in,
    )
