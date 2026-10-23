from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient



def create_presigned_download_url(config, object_name, expiration_seconds=3600):
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=object_name)
            sas_token = blob.generate_blob_sas(permission='r', expiry=expiration_seconds)
            url_with_sas = blob.url + '?' + sas_token
    return url_with_sas