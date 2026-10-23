from storage_client import get_s3_client
from typing import List


def list_prefix(bucket_name: str, prefix: str) -> List[dict]:
    client = get_s3_client()
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return response.get("Contents", [])
