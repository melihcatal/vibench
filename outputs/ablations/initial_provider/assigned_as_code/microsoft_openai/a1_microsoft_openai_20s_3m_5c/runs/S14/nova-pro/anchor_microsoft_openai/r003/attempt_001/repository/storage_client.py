from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def get_storage_client(config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        client = BlobServiceClient(config['account_url'], credential=credential)
    return client