from storage_client import get_blob_service_client
from storage_models import ObjectMetadataRequest, ObjectMetadata
from azure.core.exceptions import ResourceNotFoundError

def object_metadata(request: ObjectMetadataRequest) -> ObjectMetadata | None:
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=request.container_name, blob=request.blob_name)

    try:
        properties = blob_client.get_blob_properties()
        return ObjectMetadata(
            name=properties.name,
            size=properties.size,
            last_modified=properties.last_modified.isoformat(),
            e_tag=properties.etag,
            content_settings={
                "content_type": properties.content_settings.content_type,
                "content_encoding": properties.content_settings.content_encoding,
                "content_language": properties.content_settings.content_language,
                "content_disposition": properties.content_settings.content_disposition,
                "cache_control": properties.content_settings.cache_control
            } if properties.content_settings else {},
            metadata=properties.metadata if properties.metadata else {}
        )
    except ResourceNotFoundError:
        print(f"Blob {request.blob_name} not found in container {request.container_name}.")
        return None
    except Exception as e:
        print(f"Error retrieving blob metadata: {e}")
        return None
