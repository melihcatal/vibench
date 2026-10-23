import os
from azure.storage.blob import BlobServiceClient

def presigned_download(blob_name):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container='documents', blob=blob_name)
    download_url = blob_client.url + '?sv=2020-08-04&se=2026-09-21T22%3A00%3A00Z&sr=b&sp=r&sig=abcdefg'
    print(f'Presigned download URL: {download_url}')
    return download_url

if __name__ == '__main__':
    presigned_download('example.txt')