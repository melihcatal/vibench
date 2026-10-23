from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    client = get_storage_client()
    
    blobs = client.list_blobs(
        request.bucket_name,
        prefix=request.prefix,
        max_results=request.max_results
    )

    blob_names = [blob.name for blob in blobs]

    return ListPrefixResponse(blob_names=blob_names)
