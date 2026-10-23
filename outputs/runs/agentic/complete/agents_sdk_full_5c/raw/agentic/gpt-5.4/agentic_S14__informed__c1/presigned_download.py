from __future__ import annotations

from typing import Optional

from storage_client import get_s3_client


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in: int = 3600,
    region_name: Optional[str] = None,
    response_content_type: Optional[str] = None,
    download_filename: Optional[str] = None,
) -> str:
    s3 = get_s3_client(region_name=region_name)
    params = {"Bucket": bucket, "Key": key}
    if response_content_type:
        params["ResponseContentType"] = response_content_type
    if download_filename:
        params["ResponseContentDisposition"] = f'attachment; filename="{download_filename}"'
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=expires_in,
    )
