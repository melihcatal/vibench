from typing import Dict, List, Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_key


def list_objects_under_prefix(
    bucket: Optional[str], prefix: str
) -> Dict[str, List[Dict[str, object]]]:
    client = get_s3_client()
    response = client.list_objects_v2(
        Bucket=get_bucket_name(bucket), Prefix=normalize_key(prefix)
    )
    items = []
    for entry in response.get("Contents", []):
        items.append(
            {
                "key": entry.get("Key"),
                "size": entry.get("Size"),
                "etag": entry.get("ETag"),
                "last_modified": entry.get("LastModified"),
            }
        )
    return {
        "bucket": get_bucket_name(bucket),
        "prefix": normalize_key(prefix),
        "objects": items,
    }
