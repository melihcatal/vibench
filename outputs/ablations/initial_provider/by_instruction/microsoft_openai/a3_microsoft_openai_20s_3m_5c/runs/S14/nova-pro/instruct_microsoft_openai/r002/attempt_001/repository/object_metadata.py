import os
from azure.storage.blob import BlobServiceClient

def object_metadata(blob_name):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container='documents', blob=blob_name)
    blob_properties = blob_client.get_blob_properties()
    print(f'Metadata: {blob_properties}')
    return blob_properties

if __name__ == '__main__':
    object_metadata('example.txt')