from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def list_objects_by_prefix(config, prefix):
    credential = DefaultAzureCredential()
    client = BlobServiceClient(config['account_url'], credential=credential)
    blobs = client.get_container_client(config['container']).list_blobs(name_starts_with=prefix)
    return [blob.name for blob in blobs]
