from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def list_objects_under_prefix(prefix, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blobs = client.get_container_client(config['container']).list_blobs(name_starts_with=prefix)
            object_list = [blob.name for blob in blobs]
    return {'objects': object_list}