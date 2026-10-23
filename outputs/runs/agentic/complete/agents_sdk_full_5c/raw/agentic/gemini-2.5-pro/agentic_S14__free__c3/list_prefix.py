from typing import List
from . import storage_client

def list_objects_by_prefix(prefix: str) -> List[str]:
    """Lists objects in a GCS bucket that match a given prefix."""
    
    gcs_client = storage_client.get_storage_client()
    bucket_name = storage_client.get_default_bucket_name()
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    blobs = gcs_client.list_blobs(bucket_name, prefix=prefix)

    object_names = [blob.name for blob in blobs]
    
    print(f"Found {len(object_names)} objects with prefix '{prefix}' in bucket '{bucket_name}'.")
    return object_names
