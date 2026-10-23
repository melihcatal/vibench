'''Local helper: Azure Blob Storage client utilities.'''
import os
from azure.storage.blob import BlobServiceClient

def get_blob_service_client() -> BlobServiceClient:
    """Retrieve a configured Azure BlobServiceClient using environment variables.\n    Expected env vars: AZURE_STORAGE_ACCOUNT, AZURE_STORAGE_ACCESS_KEY or AZURE_STORAGE_CONNECTION_STRING.\n    Returns:\n        An authenticated BlobServiceClient instance.\n    """
    account = os.getenv('AZURE_STORAGE_ACCOUNT')
    if not account:
        raise RuntimeError('AZURE_STORAGE_ACCOUNT env var not set')
    # Prefer connection string if provided\n    conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    if conn_str:\n        return BlobServiceClient.from_connection_string(conn_str=conn_str)
    key = os.getenv('AZURE_STORAGE_ACCESS_KEY')
    if not key:
        raise RuntimeError('AZURE_STORAGE_ACCESS_KEY env var not set')\n    return BlobServiceClient(account_name=account, credential=key)
