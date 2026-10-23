from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_key


def create_presigned_download_url(key: str, expires_in_seconds: int = 3600) -> str:
    bucket = get_bucket_name()
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": normalize_key(key)},
        ExpiresIn=expires_in_seconds,
    )
