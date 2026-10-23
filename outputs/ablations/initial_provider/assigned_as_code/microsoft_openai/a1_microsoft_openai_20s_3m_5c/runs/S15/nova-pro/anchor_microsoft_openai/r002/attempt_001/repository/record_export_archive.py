from azure.storage.blob import BlobServiceClient


def upload_document_to_blob(document, container_name, blob_name, config=None):
    config = config or {}
    connect_str = config['connection_string']
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(document, overwrite=True)