from typing import Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_head_result


def get_object_metadata(bucket: Optional[str], key: str):
    client = get_s3_client()
    bucket_name = get_bucket_name(bucket)
    response = client.head_object(Bucket=bucket_name, Key=key)
    return normalize_head_result(bucket_name, key, response)
