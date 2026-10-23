from google.cloud import storage

from storage_client import get_bucket
from storage_models import ListedObject, normalize_prefix


def list_prefix(bucket_name: str, prefix: str = "") -> list:
    bucket = get_bucket(bucket_name)
    items = bucket.list_blobs(prefix=normalize_prefix(prefix))
    return [ListedObject(bucket=bucket_name, name=item.name, size=item.size, updated=item.updated.isoformat() if item.updated else None).to_dict() for item in items]
