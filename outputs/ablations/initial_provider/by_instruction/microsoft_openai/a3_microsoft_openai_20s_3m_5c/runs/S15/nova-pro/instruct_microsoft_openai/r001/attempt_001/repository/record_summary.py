from azure.storage.blob import BlobServiceClient

def record_summary(connection_string, container_name, blob_name, summary):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(summary, overwrite=True)