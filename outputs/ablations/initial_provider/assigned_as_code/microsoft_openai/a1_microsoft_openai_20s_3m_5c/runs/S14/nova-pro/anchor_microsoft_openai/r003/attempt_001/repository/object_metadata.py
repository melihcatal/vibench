from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def get_object_metadata(object_name, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=object_name)
            metadata = blob.get_blob_properties()
    return {'metadata': metadata}