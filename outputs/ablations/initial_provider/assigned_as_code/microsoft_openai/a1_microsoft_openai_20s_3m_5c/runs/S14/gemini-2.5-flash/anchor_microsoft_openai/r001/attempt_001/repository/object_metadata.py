from azure.storage.blob import BlobClient
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse
from storage_client import get_blob_service_client

def object_metadata(payload: ObjectMetadataRequest, config: dict = None) -> ObjectMetadataResponse:
    config = config or {}
    account_url = config['account_url']
    container_name = config['container']

    blob_service_client = get_blob_service_client(account_url)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=payload.object_name)
    
    properties = blob_client.get_blob_properties()
    
    return ObjectMetadataResponse(
        object_name=payload.object_name,
        size=properties.size,
        last_modified=properties.last_modified.isoformat(),
        content_type=properties.content_settings.content_type,
        metadata=properties.metadata
    )
