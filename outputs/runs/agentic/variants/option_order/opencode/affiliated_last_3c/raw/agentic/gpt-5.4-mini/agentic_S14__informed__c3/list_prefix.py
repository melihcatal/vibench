from typing import Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_list_result


def list_objects_with_prefix(bucket: Optional[str], prefix: str = ""):
    client = get_s3_client()
    bucket_name = get_bucket_name(bucket)
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return normalize_list_result(bucket_name, prefix, response)
