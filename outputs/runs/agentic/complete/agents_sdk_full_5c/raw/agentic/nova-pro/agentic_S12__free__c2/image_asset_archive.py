import os
from azure.storage.blob import BlobServiceClient

def archive_image_asset(image_path, container_name, blob_name):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(image_path, 'rb') as data:
        blob_client.upload_blob(data