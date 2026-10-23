from typing import Any, Dict

from storage_client import create_s3_client, get_storage_config
from storage_models import normalize_head_object_response


def object_metadata(bucket: str, key: str) -> Dict[str, Any]:
    config = get_storage_config()
    client = create_s3_client(config)
    response = client.head_object(Bucket=bucket, Key=key)
    return normalize_head_object_response(response, bucket=bucket, key=key)
