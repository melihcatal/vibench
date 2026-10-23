from storage_client import get_storage_client, get_bucket_name, get_project_id
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_prefix(payload: ListPrefixRequest):
    client = get_storage_client(get_project_id())
    bucket = client.bucket(get_bucket_name())

    blobs = client.list_blobs(bucket, prefix=payload.prefix, delimiter=payload.delimiter)

    objects = []
    for blob in blobs:
        objects.append(blob.name)
    
    prefixes = []
    for prefix in blobs.prefixes:
        prefixes.append(prefix)

    return ListPrefixResponse(objects=objects, prefixes=prefixes)
