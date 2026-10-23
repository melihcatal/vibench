from google.cloud import storage
from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject

def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    """List objects in Google Cloud Storage under a given prefix."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blobs = bucket.list_blobs(prefix=request.prefix, delimiter=request.delimiter)

    objects = [
        ListedObject(
            object_key=blob.name,
            size=blob.size,
            last_modified=blob.updated,
            etag=blob.etag
        )
        for blob in blobs
    ]

    return ListPrefixResponse(
        bucket_name=request.bucket_name,
        prefix=request.prefix,
        objects=objects
    )