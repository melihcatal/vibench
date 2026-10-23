from __future__ import annotations

from storage_client import create_s3_client, load_storage_config, normalize_boto_error
from storage_models import StorageObjectInfo, isoformat_utc


def object_metadata(key: str) -> dict:
    client = create_s3_client()
    bucket = load_storage_config().bucket
    try:
        response = client.head_object(Bucket=bucket, Key=key)
        info = StorageObjectInfo(
            key=key,
            size=response.get("ContentLength"),
            etag=response.get("ETag"),
            last_modified=isoformat_utc(response.get("LastModified")),
            content_type=response.get("ContentType"),
            metadata=response.get("Metadata"),
        )
        return info.to_dict()
    except Exception as exc:
        return {"error": normalize_boto_error(exc)}
