from storage_client import get_blob_service_client
import io

def upload_object(container_name: str, blob_name: str, data: bytes | str):
    """
    Uploads a file or byte stream to Azure Blob Storage.

    Args:
        container_name (str): The name of the container.
        blob_name (str): The name of the blob to upload.
        data (bytes | str): The data to upload, either as bytes or a string.
    """
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    if isinstance(data, str):
        data = data.encode('utf-8')

    blob_client.upload_blob(data, overwrite=True)
    return f"Successfully uploaded {blob_name} to {container_name}"
