from storage_client import AzureStorageClient
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject

def list_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    try:
        storage_client = AzureStorageClient()
        container_client = storage_client.get_container_client(request.container_name)

        blob_list = []
        for blob in container_client.list_blobs(name_starts_with=request.prefix):
            blob_list.append(ListedObject(
                name=blob.name,
                size=blob.size,
                last_modified=blob.last_modified.isoformat() if blob.last_modified else None
            ))

        return ListPrefixResponse(success=True, objects=blob_list)
    except Exception as e:
        return ListPrefixResponse(success=False, error=str(e))
