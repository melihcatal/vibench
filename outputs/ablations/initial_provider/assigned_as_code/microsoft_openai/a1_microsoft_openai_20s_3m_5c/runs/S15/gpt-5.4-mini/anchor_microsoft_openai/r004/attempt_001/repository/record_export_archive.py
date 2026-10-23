from azure.storage.blob import BlobServiceClient


def record_export_archive(payload, config=None):
    config = config or {}
    client = BlobServiceClient(account_url=config['account_url'], credential=config['sas_token'])
    container = client.get_container_client(config['container'])
    blob_name = payload['name']
    container.upload_blob(name=blob_name, data=payload['content'], overwrite=True)
    return {'name': blob_name}
