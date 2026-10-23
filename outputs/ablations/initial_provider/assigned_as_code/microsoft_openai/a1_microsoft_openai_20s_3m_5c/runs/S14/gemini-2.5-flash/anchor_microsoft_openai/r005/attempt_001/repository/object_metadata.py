from azure.storage.blob import BlobServiceClient
from storage_client import get_blob_service_client
from storage_models import StorageObjectMetadata

def object_metadata(object_name: str, config: dict) -> StorageObjectMetadata:
    account_url = config['account_url']
    container_name = config['container']

    client: BlobServiceClient = get_blob_service_client(account_url)
    blob_client = client.get_blob_client(container=container_name, blob=object_name)
    
    properties = blob_client.get_blob_properties()
    
    return StorageObjectMetadata(
        name=properties.name,
        size=properties.size,
        creation_time=properties.creation_time.isoformat(),
        last_modified_time=properties.last_modified.isoformat(),
        content_type=properties.content_settings.content_type,
        etag=properties.etag,
        metadata=properties.metadata
    )
