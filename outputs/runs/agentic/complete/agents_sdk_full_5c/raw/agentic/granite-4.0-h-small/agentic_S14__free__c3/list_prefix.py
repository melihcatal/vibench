'''List objects stored under a prefix in Azure Blob Storage.'''
from typing import List, Dict
from azure.storage.blob import BlobServiceClient
from storage_client import get_blob_service_client
from storage_models import PrefixListResult

def list_prefix(container_name: str, prefix: str = '', max_results: int = 1000) -> PrefixListResult:
    """List blobs whose names start with the given prefix.

    Args:
        container_name: Target container.
        prefix: Optional prefix filter.
        max_results: Maximum blobs to return (default 1000).\n
    Returns:
        PrefixListResult with a list of blob names and continuation token if more results.
    """
    blob_service_client = get_blob_service_client()
    blobs = blob_service_client.list_blobs(container_name, name_starts_with=prefix, max_results=max_results)
    blob_names = [blob.name for blob in blobs]
    return PrefixListResult(container=container_name, prefix=prefix, blobs=blob_names)
