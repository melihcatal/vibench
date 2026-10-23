from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_objects_with_prefix(
    request: ListPrefixRequest
) -> ListPrefixResponse:
    """Lists stored objects under a Google Cloud Storage bucket or prefix."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)

    blobs = client.list_blobs(
        bucket_or_name=bucket,
        prefix=request.prefix,
        max_results=request.max_results
    )

    object_names = []
    for blob in blobs:
        object_names.append(blob.name)

    # The Google Cloud Storage client.list_blobs method handles pagination internally
    # when iterating, so we don't directly get a next_page_token in this simple iteration.
    # For more advanced pagination, one would use `versions=True` and `page_token` parameters.

    return ListPrefixResponse(
        objects=object_names,
        next_page_token=None  # Simplified; for full pagination, adjust the client call
    )
