from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def create_storage_client(config):
    credential = DefaultAzureCredential()
    return BlobServiceClient(config['account_url'], credential=credential)
