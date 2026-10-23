from storage_client import get_blob_service_client, get_container_name
from storage_models import ObjectMetadataRequest

def object_metadata(request: ObjectMetadataRequest):
    blob_service_client = get_blob_service_client()
    container_name = get_container_name()

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=request.object_name)
    
    try:
        properties = blob_client.get_blob_properties()
        metadata = {
            "object_name": request.object_name,
            "size": properties.size,
            "creation_time": properties.creation_time.isoformat(),
            "last_modified": properties.last_modified.isoformat(),
            "etag": properties.etag,
            "content_type": properties.content_settings.content_type,
            "metadata": properties.metadata # Custom metadata
        }
        return metadata
    except Exception as e:
        return {"object_name": request.object_name, "error": str(e)}
