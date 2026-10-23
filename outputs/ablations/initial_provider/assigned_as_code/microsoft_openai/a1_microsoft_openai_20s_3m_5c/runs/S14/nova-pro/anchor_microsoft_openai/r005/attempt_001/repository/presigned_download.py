from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

def presigned_download(object_name, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=object_name)
            url = blob.url + '?sv=2020-08-04&st=2026-09-21T00:00:00Z&se=2026-09-22T00:00:00Z&sr=b&sp=r&sig=YOUR_SIGNATURE'
    return {'download_url': url}