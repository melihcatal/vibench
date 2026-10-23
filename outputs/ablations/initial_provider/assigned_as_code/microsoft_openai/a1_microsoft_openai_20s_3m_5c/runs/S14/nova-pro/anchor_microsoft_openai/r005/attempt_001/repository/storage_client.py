from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

def get_blob_client(config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        return BlobServiceClient(config['account_url'], credential=credential)