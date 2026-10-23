import os
from storage_client import ManagedStorageClient

def upload_object(bucket: str, object_key: str, file_path: str = None, byte_stream: bytes = None):
    """Upload a local file or in‑memory byte stream to managed object storage.  Uses AWS S3 compatible API via the provided ManagedStorageClient.  """
    client = ManagedStorageClient()
    if file_path:
        with open(file_path, "rb") as f:
            data = f.read()
    elif byte_stream:
        data = byte_stream
    else:
        raise ValueError("Either file_path or byte_stream must be provided.")
    client.put_object(bucket, object_key, data)
    print(f"Uploaded {object_key} to bucket {bucket}.")
