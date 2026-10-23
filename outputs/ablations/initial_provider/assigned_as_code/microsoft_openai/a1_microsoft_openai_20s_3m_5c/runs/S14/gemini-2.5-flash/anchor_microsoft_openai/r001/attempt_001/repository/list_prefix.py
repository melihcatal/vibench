from azure.storage.blob import BlobServiceClient
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject
from storage_client import get_blob_service_client

def list_prefix(payload: ListPrefixRequest, config: dict = None) -> ListPrefixResponse:
    config = config or {}
    account_url = config['account_url']
    container_name = payload.container_name or config['container']

    blob_service_client = get_blob_service_client(account_url)
    container_client = blob_service_client.get_container_client(container_name)

    blobs = []
    for blob_property in container_client.list_blobs(name_starts_with=payload.prefix):
        blobs.append(ListedObject(
            name=blob_property.name,
            size=blob_property.size,
            last_modified=blob_property.last_modified.isoformat(),
            content_type=blob_property.content_settings.content_type if blob_property.content_settings else None
        ))
    
    return ListPrefixResponse(objects=blobs)
