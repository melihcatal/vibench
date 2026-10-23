from datetime import timedelta
from typing import Optional

from storage_client import get_bucket_name, get_s3_client


def create_presigned_download_url(
    bucket: Optional[str], key: str, expires_in: int = 3600
):
    client = get_s3_client()
    bucket_name = get_bucket_name(bucket)
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": key},
        ExpiresIn=int(timedelta(seconds=expires_in).total_seconds()),
    )
