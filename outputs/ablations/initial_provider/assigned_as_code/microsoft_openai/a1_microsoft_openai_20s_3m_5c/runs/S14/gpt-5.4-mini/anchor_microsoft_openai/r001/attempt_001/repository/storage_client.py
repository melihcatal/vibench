import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def load_storage_config(config=None):
    config = dict(config or {})
    if 'account_url' not in config:
        config['account_url'] = os.environ['AZURE_STORAGE_ACCOUNT_URL']
    if 'container' not in config:
        config['container'] = os.environ['AZURE_STORAGE_CONTAINER']
    return config


def get_blob_service_client(config=None):
    config = load_storage_config(config)
    return BlobServiceClient(account_url=config['account_url'], credential=DefaultAzureCredential())
