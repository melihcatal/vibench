from __future__ import annotations

from storage_client import create_s3_client, load_storage_config, normalize_boto_error
from storage_models import StorageObjectInfo, isoformat_utc


def list_prefix(prefix: str = "", max_keys: int = 1000) -> dict:
    client = create_s3_client()
    bucket = load_storage_config().bucket
    try:
        response = client.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=max_keys)
        objects = []
        for item in response.get("Contents", []):
            objects.append(
                StorageObjectInfo(
                    key=item["Key"],
                    size=item.get("Size"),
                    etag=item.get("ETag"),
                    last_modified=isoformat_utc(item.get("LastModified")),
                ).to_dict()
            )
        return {
            "bucket": bucket,
            "prefix": prefix,
            "is_truncated": response.get("IsTruncated", False),
            "next_continuation_token": response.get("NextContinuationToken"),
            "objects": objects,
        }
    except Exception as exc:
        return {"error": normalize_boto_error(exc)}
