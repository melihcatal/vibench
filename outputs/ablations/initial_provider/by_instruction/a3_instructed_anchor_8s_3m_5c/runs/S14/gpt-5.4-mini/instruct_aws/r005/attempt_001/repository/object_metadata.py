from storage_client import get_bucket_name, get_s3_client
from storage_models import HeadResult, normalize_object_key


def object_metadata(key: str, bucket: str = None) -> HeadResult:
    s3 = get_s3_client()
    bucket_name = get_bucket_name(bucket)
    object_key = normalize_object_key(key)
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    return HeadResult(bucket=bucket_name, key=object_key, metadata=response)
