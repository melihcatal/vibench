from storage_client import get_storage_client
from storage_models import ListPrefixResponse

def list_objects_with_prefix(payload, config=None):
    config = config or {}
    client = get_storage_client()
    bucket_name = config.get("bucket")
    if not bucket_name:
        raise ValueError("Bucket name not provided in config.")

    bucket = client.bucket(bucket_name)
    prefix = payload.get("prefix", "")
    
    objects = []
    for blob in client.list_blobs(bucket_name, prefix=prefix):
        objects.append({
            "object_name": blob.name,
            "size": blob.size,
            "content_type": blob.content_type,
            "updated": blob.updated.isoformat()
        })
    
    return ListPrefixResponse(objects=objects).__dict__
