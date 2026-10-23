from storage_client import StorageClient
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse
from azure.core.exceptions import ResourceNotFoundError

def object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    client = StorageClient().get_blob_service_client()
    blob_client = client.get_blob_client(container=request.container_name, blob=request.blob_name)

    try:
        properties = blob_client.get_blob_properties()
        return ObjectMetadataResponse(
            metadata=properties.metadata if properties.metadata else {},
            size=properties.size,
            last_modified=properties.last_modified.isoformat() if properties.last_modified else "",
            etag=properties.etag
        )
    except ResourceNotFoundError:
        raise FileNotFoundError(f"Object '{request.blob_name}' not found in container '{request.container_name}'.")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve object metadata: {e}")
