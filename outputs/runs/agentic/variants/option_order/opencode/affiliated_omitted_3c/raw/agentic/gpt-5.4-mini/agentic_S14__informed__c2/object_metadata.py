from storage_client import get_default_bucket, get_s3_client
from storage_models import StorageObjectInfo, normalize_key


def object_metadata(bucket: str, key: str) -> StorageObjectInfo:
    client = get_s3_client()
    resp = client.head_object(Bucket=bucket, Key=normalize_key(key))
    return StorageObjectInfo(
        bucket=bucket,
        key=normalize_key(key),
        etag=resp.get("ETag"),
        size=resp.get("ContentLength"),
        last_modified=str(resp.get("LastModified"))
        if resp.get("LastModified")
        else None,
        content_type=resp.get("ContentType"),
        metadata=resp.get("Metadata"),
    )


def object_metadata_default(key: str) -> StorageObjectInfo:
    return object_metadata(get_default_bucket(), key)
