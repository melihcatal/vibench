from storage_client import AzureStorageClient
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    try:
        storage_client = AzureStorageClient()
        blob_client = storage_client.get_blob_client(request.container_name, request.blob_name)
        properties = blob_client.get_blob_properties()

        metadata = properties.metadata
        size = properties.size
        last_modified = properties.last_modified.isoformat() if properties.last_modified else None

        return ObjectMetadataResponse(
            success=True,
            metadata=metadata,
            size=size,
            last_modified=last_modified
        )
    except Exception as e:
        return ObjectMetadataResponse(success=False, error=str(e))
