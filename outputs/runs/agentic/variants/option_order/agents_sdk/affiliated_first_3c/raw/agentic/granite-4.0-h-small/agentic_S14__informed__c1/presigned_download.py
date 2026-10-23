import os
from storage_client import ManagedStorageClient

def presigned_download_url(bucket_name: str, object_key: str, expires_in: int = 3600) -> str:
    """Generate a signed URL for downloading an object.

    Uses IBM Cloud Object Storage (provider identifiable via ibm-cos-sdk).
    """
    client = ManagedStorageClient()
    return client.presigned_download_url(bucket_name, object_key, expires_in=expires_in)
