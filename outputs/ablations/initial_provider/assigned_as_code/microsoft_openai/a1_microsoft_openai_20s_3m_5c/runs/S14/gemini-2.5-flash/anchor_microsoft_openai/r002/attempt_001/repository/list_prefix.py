from storage_client import get_blob_service_client, get_container_name
from storage_models import ListPrefixRequest

def list_prefix(request: ListPrefixRequest):
    blob_service_client = get_blob_service_client()
    container_name = get_container_name()

    container_client = blob_service_client.get_container_client(container_name)
    
    blobs = []
    for blob in container_client.list_blobs(name_starts_with=request.prefix):
        blobs.append({
            "object_name": blob.name,
            "size": blob.size,
            "creation_time": blob.creation_time.isoformat(),
            "last_modified": blob.last_modified.isoformat(),
            "content_type": blob.content_settings.content_type,
        })
        if request.max_results and len(blobs) >= request.max_results:
            break
            
    return {"prefix": request.prefix, "objects": blobs, "count": len(blobs)}
