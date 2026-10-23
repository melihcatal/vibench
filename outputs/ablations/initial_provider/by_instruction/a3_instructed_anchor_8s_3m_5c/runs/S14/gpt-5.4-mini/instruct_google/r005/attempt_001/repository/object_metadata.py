from storage_client import get_bucket, get_object_path
from storage_models import ObjectMetadata


def object_metadata(bucket: str, key: str) -> ObjectMetadata:
    bucket_client = get_bucket(bucket)
    blob = bucket_client.blob(get_object_path(key))
    blob.reload()
    return ObjectMetadata(bucket=bucket, key=key, size=blob.size, content_type=blob.content_type, etag=blob.etag, updated=str(blob.updated) if blob.updated else None, raw=dict(blob._properties))
