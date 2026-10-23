from typing import Dict, List

from storage_client import get_bucket
from storage_models import ListObjectsResponse


def list_prefix(bucket: str, prefix: str = "") -> ListObjectsResponse:
    bucket_client = get_bucket(bucket)
    blobs = bucket_client.list_blobs(prefix=prefix)
    objects: List[Dict[str, object]] = []
    for blob in blobs:
        objects.append({"name": blob.name, "size": blob.size, "updated": str(blob.updated) if blob.updated else None, "content_type": blob.content_type, "etag": blob.etag})
    return ListObjectsResponse(bucket=bucket, prefix=prefix, objects=objects)
