from storage_client import get_s3_client, resolve_bucket_name, resolve_object_key
from storage_models import ObjectMetadataResponse, normalize_metadata


def read_object_metadata(bucket: str, key: str) -> ObjectMetadataResponse:
    client = get_s3_client()
    bucket = resolve_bucket_name(bucket)
    key = resolve_object_key(key)
    resp = client.head_object(Bucket=bucket, Key=key)
    metadata = normalize_metadata(resp.get("Metadata", {}))
    return ObjectMetadataResponse(
        bucket=bucket,
        key=key,
        etag=resp.get("ETag", "").strip('"'),
        content_length=resp.get("ContentLength", 0),
        content_type=resp.get("ContentType"),
        last_modified=resp.get("LastModified"),
        metadata=metadata,
        storage_class=resp.get("StorageClass"),
        version_id=resp.get("VersionId"),
    )
