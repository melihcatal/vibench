from storage_client import get_storage_client
from storage_models import ObjectMetadataResponse

def get_object_metadata(payload, config=None):
    config = config or {}
    client = get_storage_client()
    bucket_name = config.get("bucket")
    if not bucket_name:
        raise ValueError("Bucket name not provided in config.")

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(payload["object_name"])
    blob.reload()
    
    return ObjectMetadataResponse(
        object_name=blob.name,
        size=blob.size,
        content_type=blob.content_type,
        updated=blob.updated.isoformat()
    ).__dict__
