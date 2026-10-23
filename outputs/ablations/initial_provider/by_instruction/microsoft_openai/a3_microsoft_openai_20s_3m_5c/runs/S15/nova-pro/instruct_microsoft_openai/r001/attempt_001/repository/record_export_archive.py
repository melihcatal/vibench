from azure.storage.blob import BlobServiceClient

def record_export_archive(connection_string, container_name, blob_name, data):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(data, overwrite=True)