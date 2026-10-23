from azure.storage.blob import BlobServiceClient
import os


def record_export_archive(document_id: str, content: str, blob_name: str):
    connect_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.environ.get("AZURE_STORAGE_CONTAINER_NAME_ARCHIVE")

    if not connect_str or not container_name:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING and AZURE_STORAGE_CONTAINER_NAME_ARCHIVE environment variables must be set.")

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Get a client to interact with the specified container
    container_client = blob_service_client.get_container_client(container_name)
    
    # Create the container if it doesn't exist
    try:
        container_client.create_container()
    except Exception as e:
        # Handle case where container already exists
        if "ContainerAlreadyExists" not in str(e):
            raise

    # Get a blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the content
    blob_client.upload_blob(content, overwrite=True)
    
    return {"blob_url": blob_client.url}
