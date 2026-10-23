from azure.storage.blob import BlobServiceClient


def image_asset_archive(payload, config=None):
    config = config or {}
    client = BlobServiceClient(account_url=config['storage_account_url'], credential=config['storage_account_key'])
    container_client = client.get_container_client(config['container_name'])
    blob_client = container_client.get_blob_client(config['blob_name'])
    with open(payload['image_path'], 'rb') as data:
        blob_client.upload_blob(data)
    return {'upload_status': 'success'}