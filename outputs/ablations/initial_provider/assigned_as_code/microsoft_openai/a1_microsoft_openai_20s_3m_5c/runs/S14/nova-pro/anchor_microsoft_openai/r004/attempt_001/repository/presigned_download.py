from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def create_presigned_download_url(config, object_name, expiry_time):
    credential = DefaultAzureCredential()
    client = BlobServiceClient(config['account_url'], credential=credential)
    blob = client.get_blob_client(container=config['container'], blob=object_name)
    sas_token = blob.generate_blob_sas(permission='r', expiry=expiry_time)
    return f"{blob.url}?{sas_token}"
