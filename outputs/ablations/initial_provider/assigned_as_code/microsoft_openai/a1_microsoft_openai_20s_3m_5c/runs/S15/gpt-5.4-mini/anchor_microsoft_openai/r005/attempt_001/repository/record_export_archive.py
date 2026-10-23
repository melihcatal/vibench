from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

from database_client import load_config


def record_export_archive(payload, config=None):
    cfg = load_config(config)
    with CosmosClient(cfg['endpoint'], credential=cfg['api_key']) as client:
        container = client.get_database_client(cfg['database']).get_container_client(cfg['container'])
        item = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    blob_service = BlobServiceClient.from_connection_string(payload['storage_connection_string'])
    blob_client = blob_service.get_blob_client(container=payload['archive_container'], blob=payload['archive_name'])
    blob_client.upload_blob(str(item), overwrite=True)
    return {'archived': True, 'blob': payload['archive_name']}
