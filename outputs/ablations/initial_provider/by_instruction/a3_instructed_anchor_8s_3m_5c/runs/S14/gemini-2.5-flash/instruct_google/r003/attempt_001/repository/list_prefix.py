from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_objects_with_prefix(
    request: ListPrefixRequest
) -> ListPrefixResponse:
    """Lists stored objects under a bucket or container prefix in Google Cloud Storage."""
    client = get_storage_client()
    
    # The list_blobs method returns an iterator, so we convert it to a list of blob objects
    # and then extract the names.
    blobs = client.list_blobs(
        request.bucket_name,
        prefix=request.prefix,
        max_results=request.max_results
    )

    object_names = [blob.name for blob in blobs]

    return ListPrefixResponse(
        object_names=object_names
    )
