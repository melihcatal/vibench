from __future__ import annotations

from typing import Optional

from storage_client import get_default_bucket, get_s3_client
from storage_models import PresignedDownloadRequest


def create_presigned_download_url(request: PresignedDownloadRequest, region: Optional[str] = None) -> str:
    s3 = get_s3_client(region=region)
    bucket = get_default_bucket(request.bucket)

    params = {
        "Bucket": bucket,
        "Key": request.key,
    }
    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type

    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=request.expires_in_seconds,
    )
