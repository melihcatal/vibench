from typing import Dict, Any
from storage_client import get_s3_client
from storage_models import S3ObjectMetadata


def object_metadata(bucket: str, key: str) -> S3ObjectMetadata:
    client = get_s3_client()
    raw = client.head_object(Bucket=bucket, Key=key)
    return {
        "ETag": raw["ETag"],
        "Size": raw["ContentLength"],
        "LastModified": str(raw["LastModified"]),
        "ContentType": raw.get("ContentType"),
        "Metadata": dict(raw.get("Metadata", {})),
    }
