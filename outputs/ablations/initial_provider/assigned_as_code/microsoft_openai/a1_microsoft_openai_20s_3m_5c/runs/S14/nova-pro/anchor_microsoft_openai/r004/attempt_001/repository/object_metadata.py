from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def get_object_metadata(config, object_name):
    credential = DefaultAzureCredential()
    client = BlobServiceClient(config['account_url'], credential=credential)
    blob = client.get_blob_client(container=config['container'], blob=object_name)
    blob_properties = blob.get_blob_properties()
    return blob_properties
