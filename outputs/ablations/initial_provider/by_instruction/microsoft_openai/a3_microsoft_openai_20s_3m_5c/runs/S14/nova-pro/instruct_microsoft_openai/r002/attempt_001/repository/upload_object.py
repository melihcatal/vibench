import os
from azure.storage.blob import BlobServiceClient

def upload_object(blob_name, data):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container='documents', blob=blob_name)
    blob_client.upload_blob(data, overwrite=True)
    print(f'Uploaded {blob_name}')

if __name__ == '__main__':
    upload_object('example.txt', b'Hello, World!')