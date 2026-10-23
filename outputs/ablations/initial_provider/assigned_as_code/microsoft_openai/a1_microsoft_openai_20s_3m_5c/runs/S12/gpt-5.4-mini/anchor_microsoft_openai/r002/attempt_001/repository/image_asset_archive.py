import os

from azure.storage.blob import BlobServiceClient, ContentSettings

from vision_models import normalize_text


def image_asset_archive(payload, config=None):
    config = config or {}
    conn = config.get('connection_string') or os.environ['AZURE_STORAGE_CONNECTION_STRING']
    container = normalize_text(config.get('container') or 'image-analysis')
    name = normalize_text(payload.get('asset_name') or 'asset.json')
    data = normalize_text(payload.get('content') or '')
    service = BlobServiceClient.from_connection_string(conn)
    blob = service.get_blob_client(container=container, blob=name)
    blob.upload_blob(data.encode('utf-8'), overwrite=True, content_settings=ContentSettings(content_type='application/json'))
    return {'uri': blob.url}
