from storage_client import get_blob_client
from storage_models import ConfigType, PayloadType

def object_metadata(payload: PayloadType, config: ConfigType = None) -> PayloadType:
    config = config or {}
    container_name = config.get("container_name", payload.get("container_name"))
    object_name = payload["object_name"]

    if not all([container_name, object_name]):
        raise ValueError("Missing required parameters: container_name, object_name")

    blob_client = get_blob_client(container_name, object_name, config.get("account_url"))
    properties = blob_client.get_blob_properties()

    metadata = {
        "name": properties.name,
        "size": properties.size,
        "creation_time": properties.creation_time.isoformat() if properties.creation_time else None,
        "last_modified": properties.last_modified.isoformat() if properties.last_modified else None,
        "content_settings_content_type": properties.content_settings.content_type,
        "metadata": properties.metadata # Custom metadata
    }

    return metadata
