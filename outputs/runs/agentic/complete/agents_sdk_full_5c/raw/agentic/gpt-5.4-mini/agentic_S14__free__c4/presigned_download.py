from __future__ import annotations

from typing import Optional

from storage_client import get_bucket_name, get_s3_client


def presigned_download(key: str, expires_in: int = 3600, response_content_disposition: Optional[str] = None) -> str:
    s3 = get_s3_client()
    params = {"Bucket": get_bucket_name(), "Key": key}
    if response_content_disposition:
        params["ResponseContentDisposition"] = response_content_disposition
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=expires_in,
        HttpMethod="GET",
    )
