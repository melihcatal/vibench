from __future__ import annotations

from storage_client import get_s3_bucket, get_s3_client
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def create_presigned_download(
    request: PresignedDownloadRequest,
) -> PresignedDownloadResponse:
    client = get_s3_client()
    bucket = get_s3_bucket(request.bucket)
    params = {"Bucket": bucket, "Key": request.object_key}
    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type
    url = client.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=request.expires_in,
    )
    return PresignedDownloadResponse(
        bucket=bucket,
        object_key=request.object_key,
        url=url,
        expires_in=request.expires_in,
    )
