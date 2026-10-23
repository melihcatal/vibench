import os
from azure.storage.blob import BlobServiceClient

def metrics_export_archive(payload, config=None):
    config = config or {}
    connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    container_name = config.get('azure_blob_container_name')

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    # Get a client for the container
    container_client = blob_service_client.get_container_client(container_name)

    # Create a blob client for the new blob
    blob_name = payload['archive_filename']
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the data
    blob_client.upload_blob(payload['metric_data_content'], overwrite=True)

    return {'archive_location': f"azure_blob://{container_name}/{blob_name}"}
