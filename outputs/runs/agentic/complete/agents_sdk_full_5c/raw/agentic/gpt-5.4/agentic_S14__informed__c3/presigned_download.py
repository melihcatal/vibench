from __future__ import annotations

from typing import Optional

from storage_client import get_bucket_name, get_s3_client


def create_presigned_download_url(
    key: str,
    bucket: Optional[str] = None,
    expires_in_seconds: int = 3600,
    version_id: Optional[str] = None,
    region_name: Optional[str] = None,
) -> str:
    s3 = get_s3_client(region_name=region_name)
    params = {"Bucket": get_bucket_name(bucket), "Key": key}
    if version_id:
        params["VersionId"] = version_id
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=expires_in_seconds,
        HttpMethod="GET",
    )
