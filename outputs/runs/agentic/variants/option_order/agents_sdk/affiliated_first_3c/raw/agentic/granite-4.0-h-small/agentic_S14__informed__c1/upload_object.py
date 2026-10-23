import os
from storage_client import ManagedStorageClient

def upload_object(bucket_name: str, object_key: str, file_path: str, metadata: dict = None) -> None:
    """Upload a local file or byte stream to managed object storage.

    Uses IBM Cloud Object Storage via ibm-cos-sdk (provider identifiable).
    """
    client = ManagedStorageClient()
    client.upload_object(bucket_name, object_key, file_path, metadata=metadata)
