from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_objects_with_prefix(
    request: ListPrefixRequest
) -> ListPrefixResponse:
    """Lists stored objects under a bucket or container prefix in Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)

    blobs = client.list_blobs(bucket, prefix=request.prefix, delimiter=request.delimiter)

    object_names = []
    for blob in blobs:
        object_names.append(blob.name)
    
    prefixes = []
    for prefix in blobs.prefixes:
        prefixes.append(prefix)

    return ListPrefixResponse(
        bucket_name=request.bucket_name,
        prefix=request.prefix,
        objects=object_names,
        prefixes=prefixes,
    )
