from storage_client import get_blob_service_client, get_container_name


def list_prefix(container_name: str, prefix: str = ""):
    client = get_blob_service_client()
    container = client.get_container_client(get_container_name(container_name))
    return [item.name for item in container.list_blobs(name_starts_with=prefix)]
