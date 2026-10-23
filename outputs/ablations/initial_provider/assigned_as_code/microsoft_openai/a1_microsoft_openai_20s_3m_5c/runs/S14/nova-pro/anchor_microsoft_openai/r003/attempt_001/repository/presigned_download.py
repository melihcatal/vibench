from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def get_presigned_download_url(object_name, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=object_name)
            url = blob.url
            sas_token = blob.generate_blob_sas(permission='r', expiry=datetime.utcnow() + timedelta(hours=1))
            presigned_url = f'{url}?{sas_token}'
    return {'presigned_url': presigned_url}