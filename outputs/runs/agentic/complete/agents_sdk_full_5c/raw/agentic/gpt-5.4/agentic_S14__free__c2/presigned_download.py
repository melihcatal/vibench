from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client


DEFAULT_EXPIRATION_SECONDS = 900


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in: int = DEFAULT_EXPIRATION_SECONDS,
    version_id: Optional[str] = None,
    response_content_type: Optional[str] = None,
) -> str:
    s3 = get_s3_client()
    params = {"Bucket": bucket, "Key": key}
    if version_id:
        params["VersionId"] = version_id
    if response_content_type:
        params["ResponseContentType"] = response_content_type
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=expires_in,
        HttpMethod="GET",
    )
