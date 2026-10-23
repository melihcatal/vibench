import os
from azure.storage.blob import BlobServiceClient

def list_prefix(prefix):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client('documents')
    blob_list = container_client.list_blobs(name_starts_with=prefix)
    for blob in blob_list:
        print(blob.name)
    return blob_list

if __name__ == '__main__':
    list_prefix('example')