from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_object_key


def presigned_download_url(key: str, bucket: str = None, expires_in: int = 3600) -> str:
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": get_bucket_name(bucket), "Key": normalize_object_key(key)},
        ExpiresIn=expires_in,
    )
