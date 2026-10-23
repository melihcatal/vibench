from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def get_storage_client(config):
    with DefaultAzureCredential() as credential:
        return BlobServiceClient(config['account_url'], credential=credential)