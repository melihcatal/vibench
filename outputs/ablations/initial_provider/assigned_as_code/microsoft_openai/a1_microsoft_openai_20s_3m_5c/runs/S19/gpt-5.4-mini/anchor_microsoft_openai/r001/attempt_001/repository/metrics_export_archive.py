import base64

from azure.storage.blob import BlobServiceClient


def metrics_export_archive(payload, config=None):
    config = dict(config or {})
    client = BlobServiceClient.from_connection_string(config['connection_string'])
    container = client.get_container_client(config['container'])
    blob_name = payload['name']
    data = payload['content']
    if isinstance(data, str):
        data = data.encode('utf-8')
    if payload.get('base64'):
        data = base64.b64decode(data)
    blob = container.get_blob_client(blob_name)
    blob.upload_blob(data, overwrite=True)
    return {'uri': blob.url, 'name': blob_name}
