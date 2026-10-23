from storage_client import get_s3_client
from storage_models import head_object_to_metadata
from typing import Dict, Any


def get_object_metadata(bucket: str, key: str) -> Dict[str, Any]:
    client = get_s3_client()
    response = client.head_object(Bucket=bucket, Key=key)
    return head_object_to_metadata(response)
