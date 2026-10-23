from storage_client import get_s3_client, resolve_bucket
from storage_models import normalize_list_objects


def list_prefix(bucket, prefix=""):
    client = get_s3_client()
    response = client.list_objects_v2(Bucket=resolve_bucket(bucket), Prefix=prefix)
    return normalize_list_objects(response)
