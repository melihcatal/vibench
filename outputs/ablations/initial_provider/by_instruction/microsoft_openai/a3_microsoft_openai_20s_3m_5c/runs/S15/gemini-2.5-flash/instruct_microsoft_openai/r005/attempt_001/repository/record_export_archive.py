import os
from azure.storage.blob import BlobServiceClient, ContentSettings

def archive_document_snapshot(file_content: bytes, container_name: str, blob_name: str, content_type: str = "application/json") -> str:
    azure_storage_connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    azure_storage_account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
    azure_storage_account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")

    if not azure_storage_connection_string and (not azure_storage_account_name or not azure_storage_account_key):
        raise ValueError("Either AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY environment variables must be set.")

    try:
        if azure_storage_connection_string:
            blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
        else:
            # Construct connection string from account name and key
            connection_string = f"DefaultEndpointsProtocol=https;AccountName={azure_storage_account_name};AccountKey={azure_storage_account_key};EndpointSuffix=core.windows.net"
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(container_name)
        
        # Create container if it doesn't exist
        try:
            container_client.create_container()
            print(f"Container '{container_name}' created.")
        except Exception as e:
            # Ignore if container already exists
            if "ContainerAlreadyExists" not in str(e):
                raise e

        blob_client = container_client.get_blob_client(blob_name)
        content_settings = ContentSettings(content_type=content_type)
        blob_client.upload_blob(file_content, content_settings=content_settings, overwrite=True)

        return f"Successfully archived '{blob_name}' to container '{container_name}'. URL: {blob_client.url}"
    except Exception as e:
        return f"Error archiving document snapshot: {e}"

if __name__ == "__main__":
    # Example usage
    sample_document_data = {"id": "snapshot_123", "timestamp": "2026-09-20T10:00:00Z", "data": {"name": "Archived Doc", "version": 1}}
    import json
    file_content_bytes = json.dumps(sample_document_data).encode('utf-8')
    
    archive_container_name = "document-snapshots"
    archive_blob_name = f"snapshot_{sample_document_data['id']}.json"

    # Ensure AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY
    # environment variables are set.
    if not (os.environ.get("AZURE_STORAGE_CONNECTION_STRING") or \
            (os.environ.get("AZURE_STORAGE_ACCOUNT_NAME") and os.environ.get("AZURE_STORAGE_ACCOUNT_KEY"))):
        print("Please set AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY environment variables to run this example.")
    else:
        archive_result = archive_document_snapshot(file_content_bytes, archive_container_name, archive_blob_name)
        print(archive_result)
