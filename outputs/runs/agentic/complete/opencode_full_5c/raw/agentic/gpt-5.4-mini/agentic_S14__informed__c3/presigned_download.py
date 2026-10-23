from datetime import timedelta
from typing import Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_key


def create_presigned_download_url(
    bucket: Optional[str], key: str, expires_in: int = 900
) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": get_bucket_name(bucket), "Key": normalize_key(key)},
        ExpiresIn=int(timedelta(seconds=expires_in).total_seconds()),
    )
