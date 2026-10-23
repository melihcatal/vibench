from storage_client import StorageClient
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    client = StorageClient().get_blob_service_client()
    container_client = client.get_container_client(request.container_name)

    blob_names = []
    try:
        for blob in container_client.list_blobs(name_starts_with=request.prefix):
            blob_names.append(blob.name)
    except Exception as e:
        raise RuntimeError(f"Failed to list blobs with prefix: {e}")

    return ListPrefixResponse(blob_names=blob_names)
