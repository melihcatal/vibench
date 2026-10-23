import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def load_storage_config(config=None):
    base = dict(config or {})
    if 'account_url' not in base:
        base['account_url'] = os.environ.get('AZURE_STORAGE_ACCOUNT_URL')
    if 'container' not in base:
        base['container'] = os.environ.get('AZURE_STORAGE_CONTAINER')
    return base


def get_blob_service_client(config=None):
    resolved = load_storage_config(config)
    return BlobServiceClient(resolved['account_url'], credential=DefaultAzureCredential())
