import os
from storage_client import get_s3_client
from storage_models import ListObjectsResult, normalize_list_objects_response

def list_objects_by_prefix(bucket_name: str, prefix: str = '', delimiter: str = '/') -> ListObjectsResult:
    s3_client = get_s3_client()
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix,
        Delimiter=delimiter
    )
    return normalize_list_objects_response(response)
