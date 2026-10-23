from storage_client import get_blob_service_client

def get_object_metadata(container_name: str, blob_name: str):
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    properties = blob_client.get_blob_properties()
    metadata = {k: v for k, v in properties.metadata.items()} if properties.metadata else {}
    return {
        "name": properties.name,
        "container": properties.container,
        "size": properties.size,
        "creation_time": properties.creation_time.isoformat() if properties.creation_time else None,
        "last_modified": properties.last_modified.isoformat() if properties.last_modified else None,
        "content_settings": {
            "content_type": properties.content_settings.content_type,
            "content_md5": properties.content_settings.content_md5,
        },
        "metadata": metadata
    }
