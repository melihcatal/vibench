from storage_client import get_container_client
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    container_client = get_container_client(request.container_name)
    blob_names = []
    for blob in container_client.list_blobs(name_starts_with=request.prefix):
        blob_names.append(blob.name)
    return ListPrefixResponse(blobs=blob_names)
