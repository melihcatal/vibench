from google.cloud import storage
from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_objects_with_prefix(payload: ListPrefixRequest, config=None):
    config = config or {}
    client = get_storage_client(config["project_id"])
    
    # The GCS client.list_blobs method requires a bucket object
    bucket = client.bucket(payload.bucket_name)

    blobs = client.list_blobs(bucket, prefix=payload.prefix)
    object_names = [blob.name for blob in blobs]

    return ListPrefixResponse(object_names=object_names)
