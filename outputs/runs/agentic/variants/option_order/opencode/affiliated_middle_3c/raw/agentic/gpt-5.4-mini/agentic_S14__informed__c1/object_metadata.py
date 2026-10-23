from storage_client import get_bucket_name, get_s3_client
from storage_models import ObjectMetadataResult, normalize_key


def read_object_metadata(key: str) -> ObjectMetadataResult:
    bucket = get_bucket_name()
    s3 = get_s3_client()
    response = s3.head_object(Bucket=bucket, Key=normalize_key(key))
    return ObjectMetadataResult(
        bucket=bucket, key=normalize_key(key), metadata=response
    )
