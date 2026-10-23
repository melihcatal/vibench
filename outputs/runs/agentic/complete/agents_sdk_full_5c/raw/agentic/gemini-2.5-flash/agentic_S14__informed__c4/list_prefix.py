from google.cloud import storage
from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ObjectSummary

def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    """Lists stored objects under a bucket or container prefix in Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)

    blobs = client.list_blobs(bucket, prefix=request.prefix, delimiter=request.delimiter)

    objects = []
    for blob in blobs:
        objects.append(ObjectSummary(name=blob.name, size=blob.size, updated=blob.updated.isoformat() if blob.updated else None))
    
    # Also include prefixes if a delimiter was used
    prefixes = list(blobs.prefixes)

    return ListPrefixResponse(
        bucket_name=request.bucket_name,
        prefix=request.prefix,
        objects=objects,
        common_prefixes=prefixes
    )
