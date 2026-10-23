from __future__ import annotations

from storage_client import require_bucket, s3_client
from storage_models import PresignedDownload


S3_PROVIDER = "Amazon S3"


def create_presigned_download(bucket: str, key: str, expires_in: int = 3600, response_content_type: str | None = None) -> PresignedDownload:
    client = s3_client()
    resolved_bucket = require_bucket(bucket)
    params = {"Bucket": resolved_bucket, "Key": key}
    if response_content_type:
        params["ResponseContentType"] = response_content_type
    url = client.generate_presigned_url("get_object", Params=params, ExpiresIn=expires_in)
    return PresignedDownload(bucket=resolved_bucket, key=key, url=url, expires_in=expires_in)


def create_presigned_download_dict(bucket: str, key: str, expires_in: int = 3600) -> dict:
    return create_presigned_download(bucket=bucket, key=key, expires_in=expires_in).to_dict()
