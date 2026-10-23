from storage_client import get_container_client
from storage_models import ConfigType, PayloadType

def list_prefix(payload: PayloadType, config: ConfigType = None) -> PayloadType:
    config = config or {}
    container_name = config.get("container_name", payload.get("container_name"))
    prefix = payload.get("prefix", "")
    max_results = payload.get("max_results")

    if not container_name:
        raise ValueError("Missing required parameter: container_name")

    container_client = get_container_client(container_name, config.get("account_url"))
    
    blob_list = []
    for blob in container_client.list_blobs(name_starts_with=prefix):
        blob_list.append({
            "name": blob.name,
            "size": blob.size,
            "last_modified": blob.last_modified.isoformat() if blob.last_modified else None,
            "creation_time": blob.creation_time.isoformat() if blob.creation_time else None,
            "content_settings_content_type": blob.content_settings.content_type,
        })
        if max_results and len(blob_list) >= max_results:
            break

    return {"objects": blob_list}
