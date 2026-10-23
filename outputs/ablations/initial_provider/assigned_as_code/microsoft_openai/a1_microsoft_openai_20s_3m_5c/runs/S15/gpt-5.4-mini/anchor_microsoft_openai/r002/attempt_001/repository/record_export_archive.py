from azure.storage.blob import BlobServiceClient


def record_export_archive(payload, config=None):
    config = config or {}
    service = BlobServiceClient.from_connection_string(config['blob_connection_string'])
    container = service.get_container_client(config['blob_container'])
    blob = container.get_blob_client(payload['archive_name'])
    blob.upload_blob(payload['content'], overwrite=True)
    return {'archive_name': payload['archive_name']}
