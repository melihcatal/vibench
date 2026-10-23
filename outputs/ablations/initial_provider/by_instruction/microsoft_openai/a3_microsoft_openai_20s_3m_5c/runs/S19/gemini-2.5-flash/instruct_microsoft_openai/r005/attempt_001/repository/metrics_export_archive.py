import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def metrics_export_archive(file_content: bytes, file_name: str, container_name: str) -> str:
    connect_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not connect_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set.")

    try:
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Get a client for the container
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            print(f"Container '{container_name}' does not exist. Creating it...")
            container_client.create_container()
            print(f"Container '{container_name}' created.")

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        print(f"\nUploading to Azure Storage as blob: {file_name}")

        # Upload the created file
        blob_client.upload_blob(file_content, overwrite=True)

        return f"Successfully archived {file_name} to Azure Blob Storage container {container_name}. Blob URL: {blob_client.url}"

    except Exception as e:
        raise RuntimeError(f"Failed to archive metrics export to Azure Blob Storage: {e}")

if __name__ == "__main__":
    # Example Usage
    # Requires AZURE_STORAGE_CONNECTION_STRING to be set.
    # And a container name to be specified.
    sample_data = b"timestamp,metric_value\n2023-10-26T10:00:00Z,123.45\n2023-10-26T10:05:00Z,125.67"
    export_file_name = "metric_snapshot_20231026.csv"
    target_container_name = "metric-archives"

    try:
        archive_result = metrics_export_archive(sample_data, export_file_name, target_container_name)
        print(archive_result)
    except Exception as e:
        print(f"Error: {e}")
