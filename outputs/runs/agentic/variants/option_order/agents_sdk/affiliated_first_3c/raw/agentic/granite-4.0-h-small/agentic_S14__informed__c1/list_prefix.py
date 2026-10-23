import os
from storage_client import ManagedStorageClient

def list_objects_by_prefix(bucket_name: str, prefix: str, delimiter: str = None) -> list:
    """List objects stored under a given prefix.

    Uses IBM Cloud Object Storage (provider identifiable via ibm-cos-sdk).
    """
    client = ManagedStorageClient()
    return client.list_objects(bucket_name, prefix, delimiter=delimiter)
