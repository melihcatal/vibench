from storage_client import get_storage_client
from typing import Any


def create_presigned_download_url(
    bucket: str, object_key: str, expiration_seconds: int = 3600
) -> str:
    client = get_storage_client()
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": object_key},
        ExpiresIn=expiration_seconds,
    )
    return url
