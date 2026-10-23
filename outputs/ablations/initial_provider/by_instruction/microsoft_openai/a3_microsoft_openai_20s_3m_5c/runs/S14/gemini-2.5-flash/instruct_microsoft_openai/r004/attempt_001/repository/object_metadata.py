from storage_client import get_blob_service_client

def get_object_metadata(container_name: str, blob_name: str) -> dict:
    """
    Reads object metadata from Azure Blob Storage.

    Args:
        container_name (str): The name of the container.
        blob_name (str): The name of the blob.

    Returns:
        dict: A dictionary containing the blob properties (metadata).
    """
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    properties = blob_client.get_blob_properties()
    return {
        "name": properties.name,
        "size": properties.size,
        "creation_time": properties.creation_time.isoformat() if properties.creation_time else None,
        "last_modified": properties.last_modified.isoformat() if properties.last_modified else None,
        "etag": properties.etag,
        "content_settings": properties.content_settings.__dict__,
        "metadata": properties.metadata,
    }
