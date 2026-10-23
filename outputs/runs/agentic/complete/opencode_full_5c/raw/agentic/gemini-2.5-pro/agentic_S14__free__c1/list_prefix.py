from storage_client import get_storage_client
from typing import List


def list_objects_with_prefix(bucket_name: str, prefix: str) -> List[str]:
    """Lists blobs in a bucket that begin with the prefix."""
    storage_client = get_storage_client()
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)

    blob_names = [blob.name for blob in blobs]

    print(f"Blobs in gs://{bucket_name} with prefix '{prefix}':")
    for blob_name in blob_names:
        print(blob_name)

    return blob_names
