from storage_client import get_blob_service_client

def list_objects_with_prefix(container_name: str, prefix: str = ""):
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = []
    for blob in container_client.list_blobs(name_starts_with=prefix):
        blob_list.append({
            "name": blob.name,
            "size": blob.size,
            "last_modified": blob.last_modified.isoformat() if blob.last_modified else None,
            "etag": blob.etag,
            "content_settings": {
                "content_type": blob.content_settings.content_type,
            }
        })
    return blob_list
