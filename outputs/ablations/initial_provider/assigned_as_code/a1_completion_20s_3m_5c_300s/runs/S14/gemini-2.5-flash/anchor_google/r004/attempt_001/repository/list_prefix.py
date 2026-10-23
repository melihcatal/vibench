from storage_client import get_storage_client
from storage_models import StorageListResponse, StorageObject
from typing import List

def list_prefix(payload: dict) -> StorageListResponse:
    client = get_storage_client()
    bucket = client.bucket(payload["bucket_name"])
    
    # The 'prefix' parameter filters objects whose names begin with this prefix.
    blobs = client.list_blobs(bucket, prefix=payload.get("prefix"))
    
    objects: List[StorageObject] = []
    for blob in blobs:
        objects.append({
            "name": blob.name,
            "bucket": blob.bucket.name,
            "size": blob.size,
            "content_type": blob.content_type,
            "time_created": blob.time_created.isoformat() if blob.time_created else None,
            "updated": blob.updated.isoformat() if blob.updated else None,
        })
    
    return {"objects": objects}
