import base64

from azure.storage.blob import BlobServiceClient


def metrics_export_archive(payload, config=None):
    config = config or {}
    data = payload.get('data') or payload.get('content') or ''
    blob_name = payload.get('blob_name') or 'metrics-export.json'
    connection_string = config.get('azure_storage_connection_string')
    container_name = config.get('container_name')
    if connection_string and container_name:
        client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(data if isinstance(data, (bytes, bytearray)) else str(data).encode('utf-8'), overwrite=True)
        uri = blob_client.url
    else:
        uri = 'data:application/octet-stream;base64,' + base64.b64encode(data if isinstance(data, (bytes, bytearray)) else str(data).encode('utf-8')).decode('ascii')
    return {'blob_name': blob_name, 'uri': uri}
