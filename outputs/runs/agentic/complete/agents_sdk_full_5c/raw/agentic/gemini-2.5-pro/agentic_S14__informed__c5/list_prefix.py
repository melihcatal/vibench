from google.cloud import storage
from storage_client import get_storage_client, get_bucket_name
from typing import List

def list_objects_with_prefix(prefix: str) -> List[str]:
    """Lists all the blobs in the bucket with a given prefix."""
    storage_client = get_storage_client()
    bucket_name = get_bucket_name()
    
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)

    object_names = []
    print(f"Blobs in gs://{bucket_name} with prefix '{prefix}':")
    for blob in blobs:
        print(blob.name)
        object_names.append(blob.name)
    
    return object_names
