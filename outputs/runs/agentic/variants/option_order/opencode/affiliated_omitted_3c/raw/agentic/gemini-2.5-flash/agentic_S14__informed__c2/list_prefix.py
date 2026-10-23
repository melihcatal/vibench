from storage_client import get_blob_service_client
from storage_models import ListPrefixRequest, ListPrefixResponse


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(request.container_name)

    blob_names = []
    for blob in container_client.list_blobs(name_starts_with=request.prefix):
        blob_names.append(blob.name)

    return ListPrefixResponse(blob_names=blob_names)
