from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client, require_bucket


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in: int = 3600,
    version_id: Optional[str] = None,
    region_name: Optional[str] = None,
) -> str:
    s3 = get_s3_client(region_name)
    params = {"Bucket": require_bucket(bucket), "Key": key}
    if version_id:
        params["VersionId"] = version_id
    return s3.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=expires_in,
        HttpMethod="GET",
    )
