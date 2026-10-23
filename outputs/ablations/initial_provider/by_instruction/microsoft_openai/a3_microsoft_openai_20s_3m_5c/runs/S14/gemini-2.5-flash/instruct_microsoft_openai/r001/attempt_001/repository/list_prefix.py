from storage_client import AzureBlobStorageClient
from storage_models import ListPrefixRequest, ListPrefixResponse
from azure.core.exceptions import ResourceNotFoundError

def list_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    client = AzureBlobStorageClient()
    try:
        container_client = client.blob_service_client.get_container_client(request.container_name)
        blob_names = []
        for blob in container_client.list_blobs(name_starts_with=request.prefix):
            blob_names.append(blob.name)
        return ListPrefixResponse(success=True, blob_names=blob_names)
    except ResourceNotFoundError:
        return ListPrefixResponse(success=False, error=f"Container '{request.container_name}' not found.")
    except Exception as e:
        return ListPrefixResponse(success=False, error=str(e))
