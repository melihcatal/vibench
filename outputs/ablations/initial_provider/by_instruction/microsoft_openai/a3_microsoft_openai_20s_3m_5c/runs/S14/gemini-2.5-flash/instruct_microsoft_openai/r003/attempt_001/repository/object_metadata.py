from storage_client import get_blob_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    blob_client = get_blob_client(request.container_name, request.blob_name)
    properties = blob_client.get_blob_properties()

    return ObjectMetadataResponse(
        name=properties.name,
        size=properties.size,
        content_settings=properties.content_settings,
        metadata=properties.metadata
    )
