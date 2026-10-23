from storage_client import get_default_bucket, get_s3_client
from storage_models import StorageListResult, normalize_prefix


def list_prefix(bucket: str, prefix: str = "") -> StorageListResult:
    client = get_s3_client()
    resp = client.list_objects_v2(Bucket=bucket, Prefix=normalize_prefix(prefix))
    keys = [item["Key"] for item in resp.get("Contents", [])]
    return StorageListResult(bucket=bucket, prefix=normalize_prefix(prefix), keys=keys)


def list_default_prefix(prefix: str = "") -> StorageListResult:
    return list_prefix(get_default_bucket(), prefix=prefix)
