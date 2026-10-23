import os
from storage_client import get_s3_client
from storage_models import ObjectMetadata, normalize_head_object_response

def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadata:
    s3_client = get_s3_client()
    response = s3_client.head_object(
        Bucket=bucket_name,
        Key=object_key
    )
    return normalize_head_object_response(object_key, response)
