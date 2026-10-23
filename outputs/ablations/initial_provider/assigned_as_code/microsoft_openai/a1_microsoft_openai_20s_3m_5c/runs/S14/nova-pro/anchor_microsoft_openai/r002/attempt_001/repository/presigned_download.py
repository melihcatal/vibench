from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def create_presigned_download_url(config, object_name, expiry_seconds):
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=object_name)
            url = blob.generate_sas(permission='r', expiry=expiry_seconds)
            return url