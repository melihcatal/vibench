from storage_client import get_bucket_name, get_default_prefix, get_s3_client
from storage_models import normalize_listed_objects


def list_prefix(bucket: str = None, prefix: str = None):
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=get_bucket_name(bucket), Prefix=get_default_prefix(prefix))
    contents = response.get("Contents", [])
    return normalize_listed_objects(contents)
