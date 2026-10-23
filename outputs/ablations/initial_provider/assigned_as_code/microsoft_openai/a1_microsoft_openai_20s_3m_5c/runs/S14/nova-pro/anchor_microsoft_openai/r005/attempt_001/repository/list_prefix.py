from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

def list_prefix(prefix, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blobs = client.list_blobs(config['container'], name_starts_with=prefix)
            object_list = [blob.name for blob in blobs]
    return object_list