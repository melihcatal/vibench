from typing import Any, Dict, Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_key, normalize_metadata


def read_object_metadata(bucket: Optional[str], key: str) -> Dict[str, Any]:
    client = get_s3_client()
    response = client.head_object(
        Bucket=get_bucket_name(bucket), Key=normalize_key(key)
    )
    return {
        "bucket": get_bucket_name(bucket),
        "key": normalize_key(key),
        "content_length": response.get("ContentLength"),
        "content_type": response.get("ContentType"),
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified"),
        "metadata": normalize_metadata(response.get("Metadata")),
    }
