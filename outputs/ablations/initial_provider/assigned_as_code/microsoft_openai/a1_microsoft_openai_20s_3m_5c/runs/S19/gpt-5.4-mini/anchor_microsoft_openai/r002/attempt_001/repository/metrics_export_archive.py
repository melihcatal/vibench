import base64
from azure.storage.blob import BlobServiceClient


def metrics_export_archive(payload, config=None):
    connection_string = (config or {}).get('connection_string') or payload.get('connection_string')
    container_name = (config or {}).get('container') or payload.get('container')
    blob_name = payload['blob_name']
    content = payload['content']
    if isinstance(content, str):
        content = content.encode('utf-8')
    elif isinstance(content, bytes):
        pass
    else:
        content = base64.b64decode(content)
    client = BlobServiceClient.from_connection_string(connection_string)
    blob = client.get_blob_client(container=container_name, blob=blob_name)
    blob.upload_blob(content, overwrite=True)
    return {'archived': True, 'blob_name': blob_name}
