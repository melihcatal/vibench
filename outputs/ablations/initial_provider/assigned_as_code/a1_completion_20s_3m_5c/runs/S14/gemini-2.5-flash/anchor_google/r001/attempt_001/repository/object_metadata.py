from storage_client import get_storage_client, get_bucket_name, get_project_id
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def object_metadata(payload: ObjectMetadataRequest):
    client = get_storage_client(get_project_id())
    bucket = client.bucket(get_bucket_name())
    blob = bucket.blob(payload.object_name)
    
    blob.reload()
    
    return ObjectMetadataResponse(
        object_name=blob.name,
        size=blob.size,
        content_type=blob.content_type,
        etag=blob.etag,
        updated=str(blob.updated),
        metadata=blob.metadata
    )
