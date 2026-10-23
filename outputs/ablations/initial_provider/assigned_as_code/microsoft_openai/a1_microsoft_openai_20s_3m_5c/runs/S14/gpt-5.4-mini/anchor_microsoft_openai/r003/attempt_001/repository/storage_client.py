from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def build_blob_service_client(config=None):
    config = config or {}
    account_url = config['account_url']
    return BlobServiceClient(account_url, credential=DefaultAzureCredential())


def get_blob_client(config=None, object_name=None):
    config = config or {}
    client = build_blob_service_client(config)
    return client.get_blob_client(container=config['container'], blob=object_name)
