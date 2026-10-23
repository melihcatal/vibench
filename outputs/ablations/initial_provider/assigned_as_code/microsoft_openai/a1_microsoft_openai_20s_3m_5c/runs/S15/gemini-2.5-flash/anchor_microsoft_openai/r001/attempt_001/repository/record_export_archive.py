from azure.storage.blob import BlobServiceClient
import os

def record_export_archive(file_content, file_name, container_name="document-archives"):
    connect_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not connect_str:
        return {'success': False, 'message': 'Azure Storage connection string not found.'}

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    try:
        # Create a blob client for the specific blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        # Upload the file content
        blob_client.upload_blob(file_content, overwrite=True)

        return {'success': True, 'blob_url': blob_client.url}
    except Exception as e:
        print(f"Error archiving document to Azure Blob Storage: {e}")
        return {'success': False, 'message': str(e)}
