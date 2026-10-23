from storage_client import get_bucket_name, get_s3_client
from storage_models import ListObjectsResult, normalize_prefix


def list_objects_by_prefix(prefix: str = "") -> ListObjectsResult:
    bucket = get_bucket_name()
    s3 = get_s3_client()
    normalized_prefix = normalize_prefix(prefix)
    response = s3.list_objects_v2(Bucket=bucket, Prefix=normalized_prefix)
    keys = [item["Key"] for item in response.get("Contents", [])]
    return ListObjectsResult(bucket=bucket, prefix=normalized_prefix, keys=keys)
