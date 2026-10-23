from typing import Any, Dict, List, Optional

from storage_client import create_s3_client, get_storage_config
from storage_models import normalize_list_objects_response


def list_prefix(bucket: str, prefix: str = "", max_keys: Optional[int] = None) -> Dict[str, Any]:
    config = get_storage_config()
    client = create_s3_client(config)
    params = {"Bucket": bucket, "Prefix": prefix}
    if max_keys is not None:
        params["MaxKeys"] = max_keys
    response = client.list_objects_v2(**params)
    return normalize_list_objects_response(response, bucket=bucket, prefix=prefix)
