from datetime import timedelta
from typing import Optional

from storage_client import create_s3_client, get_storage_config
from storage_models import PresignedURL


def presigned_download(bucket: str, key: str, expires_in_seconds: int = 3600, response_content_disposition: Optional[str] = None) -> PresignedURL:
    config = get_storage_config()
    client = create_s3_client(config)
    params = {"Bucket": bucket, "Key": key}
    if response_content_disposition:
        params["ResponseContentDisposition"] = response_content_disposition
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=expires_in_seconds,
    )
    return PresignedURL(url=url, expires_in_seconds=expires_in_seconds)
