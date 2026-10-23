from datetime import timedelta
from typing import Optional

from botocore.exceptions import BotoCoreError, ClientError

from storage_client import get_s3_client, resolve_bucket_name, resolve_object_key
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def create_presigned_download_url(request: PresignedDownloadRequest) -> PresignedDownloadResponse:
    client = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    key = resolve_object_key(request.key)
    expires_in = int(request.expires_in_seconds or timedelta(hours=1).total_seconds())
    params = {"Bucket": bucket, "Key": key}
    if request.response_content_disposition:
        params["ResponseContentDisposition"] = request.response_content_disposition
    if request.response_content_type:
        params["ResponseContentType"] = request.response_content_type
    try:
        url = client.generate_presigned_url("get_object", Params=params, ExpiresIn=expires_in)
        return PresignedDownloadResponse(bucket=bucket, key=key, url=url, expires_in_seconds=expires_in)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"failed to create presigned url for s3://{bucket}/{key}: {exc}") from exc


__all__ = ["create_presigned_download_url"]
