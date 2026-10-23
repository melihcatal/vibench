import base64

from azure.storage.blob import BlobServiceClient


def image_asset_archive(payload, config=None):
    config = dict(config or {})
    client = BlobServiceClient.from_connection_string(config['connection_string'])
    container = client.get_container_client(config['container'])
    asset_id = config.get('asset_id', 'image-analysis')
    blob = container.get_blob_client(f"{asset_id}.json")
    data = payload.get('artifact', b'')
    if isinstance(data, str):
        data = data.encode('utf-8')
    blob.upload_blob(data, overwrite=True)
    return {'uri': blob.url, 'digest': base64.b64encode(data).decode('utf-8')}
