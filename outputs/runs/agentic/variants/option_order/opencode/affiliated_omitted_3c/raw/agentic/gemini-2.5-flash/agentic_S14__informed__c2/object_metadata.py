from storage_client import get_blob_service_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(
        container=request.container_name, blob=request.blob_name
    )

    properties = blob_client.get_blob_properties()

    return ObjectMetadataResponse(
        name=properties.name,
        etag=properties.etag,
        last_modified=str(properties.last_modified),
        size=properties.size,
        content_type=properties.content_settings.content_type,
        metadata=properties.metadata,
    )
