import os
from storage_client import get_managed_storage_client


def upload_object(bucket_name, object_key, file_path=None, byte_stream=None):
    """Upload a file or byte stream to managed object storage.

    Uses ibm-cos-sdk to interact with IBM Cloud Object Storage.
    """
    cos = get_managed_storage_client()
    if file_path:
        with open(file_path, "rb") as f:
            cos.put_object(Bucket=bucket_name, Key=object_key, Body=f)
    elif byte_stream:
        cos.put_object(Bucket=bucket_name, Key=object_key, Body=byte_stream)
    else:
        raise ValueError("Provide either file_path or byte_stream")
