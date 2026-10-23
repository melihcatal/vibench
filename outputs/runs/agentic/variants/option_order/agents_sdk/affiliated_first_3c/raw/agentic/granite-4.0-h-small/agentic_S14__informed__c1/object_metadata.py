import os
from storage_client import ManagedStorageClient

def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """Retrieve metadata / HEAD information for an object.

    IBM Cloud Object Storage via ibm-cos-sdk (provider identifiable).
    """
    client = ManagedStorageClient()
    return client.get_object_metadata(bucket_name, object_key)
