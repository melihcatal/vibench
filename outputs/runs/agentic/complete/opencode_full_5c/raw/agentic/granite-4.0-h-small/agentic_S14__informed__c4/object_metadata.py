import os
from storage_client import get_managed_storage_client


def get_object_metadata(bucket_name, object_key):
    """Retrieve object metadata (HEAD request) from managed storage.

    Uses ibm-cos-sdk to fetch metadata for IBM Cloud Object Storage.
    """
    cos = get_managed_storage_client()
    response = cos.head_object(Bucket=bucket_name, Key=object_key)
    return response
