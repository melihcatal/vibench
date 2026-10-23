from azure.storage.blob import BlobServiceClient


def metrics_export_archive(payload, config=None):
    config = config or {}
    client = BlobServiceClient.from_connection_string(config['connection_string'])
    blob = client.get_blob_client(container=config['container'], blob=payload['blob_name'])
    blob.upload_blob(payload['content'], overwrite=True)
    return {'archived': True, 'blob_url': blob.url}
