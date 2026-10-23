from storage_client import get_blob_service_client, get_container_name, to_dict


def object_metadata(container_name: str, object_name: str):
    client = get_blob_service_client()
    blob_client = client.get_blob_client(container=get_container_name(container_name), blob=object_name)
    props = blob_client.get_blob_properties()
    return {
        "container_name": container_name,
        "object_name": object_name,
        "size": props.size,
        "content_type": props.content_settings.content_type if props.content_settings else None,
        "etag": props.etag,
        "last_modified": props.last_modified.isoformat() if props.last_modified else None,
        "metadata": to_dict(props.metadata),
    }
