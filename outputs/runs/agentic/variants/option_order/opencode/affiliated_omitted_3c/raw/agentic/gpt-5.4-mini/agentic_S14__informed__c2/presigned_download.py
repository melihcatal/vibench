from storage_client import get_default_bucket, get_s3_client
from storage_models import normalize_key


def presigned_download(bucket: str, key: str, expires_in: int = 900) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": normalize_key(key)},
        ExpiresIn=expires_in,
    )


def presigned_download_default(key: str, expires_in: int = 900) -> str:
    return presigned_download(get_default_bucket(), key, expires_in=expires_in)
