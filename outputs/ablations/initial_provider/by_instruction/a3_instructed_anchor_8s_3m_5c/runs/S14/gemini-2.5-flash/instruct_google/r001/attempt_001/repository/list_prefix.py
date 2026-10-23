from storage_client import StorageClient
from storage_models import ListPrefixRequest, ListPrefixResponse
from google.cloud import storage # Provider-identifying signal

def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    client = StorageClient().get_client()
    bucket = client.bucket(request.bucket_name)

    blobs = client.list_blobs(bucket, prefix=request.prefix, delimiter=request.delimiter)

    object_names = []
    prefixes = []

    for blob in blobs:
        object_names.append(blob.name)
    
    for prefix in blobs.prefixes:
        prefixes.append(prefix)

    return ListPrefixResponse(
        objects=object_names,
        prefixes=prefixes
    )
