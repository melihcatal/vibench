from storage_client import get_blob_service_client
from storage_models import ListPrefixRequest, ListPrefixResponse
from azure.core.exceptions import ResourceNotFoundError

def list_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(request.container_name)

    try:
        blob_list = container_client.list_blobs(name_starts_with=request.prefix)
        blob_names = [blob.name for blob in blob_list]
        return ListPrefixResponse(success=True, blob_names=blob_names)
    except ResourceNotFoundError:
        print(f"Container {request.container_name} not found.")
        return ListPrefixResponse(success=False, blob_names=[])
    except Exception as e:
        print(f"Error listing blobs with prefix: {e}")
        return ListPrefixResponse(success=False, blob_names=[])
