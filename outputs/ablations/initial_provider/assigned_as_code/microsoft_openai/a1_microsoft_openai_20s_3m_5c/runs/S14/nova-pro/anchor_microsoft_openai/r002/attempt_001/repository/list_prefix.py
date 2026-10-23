from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def list_objects_with_prefix(config, prefix):
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blobs = client.get_container_client(config['container']).list_blobs(name_starts_with=prefix)
            return [blob.name for blob in blobs]