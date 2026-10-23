from storage_client import get_bucket
from storage_models import StorageObjectResponse, normalize_object_name


def read_object_metadata(bucket: str, object_name: str) -> StorageObjectResponse:
    blob = get_bucket(bucket).blob(normalize_object_name(object_name))
    blob.reload()
    return StorageObjectResponse(bucket=bucket, object_name=blob.name, uri=f"gs://{bucket}/{blob.name}", etag=blob.etag, size=blob.size, content_type=blob.content_type, metadata=dict(blob.metadata or {}))
