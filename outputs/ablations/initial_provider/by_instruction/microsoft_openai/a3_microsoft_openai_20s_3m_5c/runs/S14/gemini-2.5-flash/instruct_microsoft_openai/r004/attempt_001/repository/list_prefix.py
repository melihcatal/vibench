from storage_client import get_blob_service_client

def list_objects_with_prefix(container_name: str, prefix: str | None = None) -> list[dict]:
    """
    Lists stored objects under a bucket or container prefix in Azure Blob Storage.

    Args:
        container_name (str): The name of the container.
        prefix (str | None): The prefix to filter blobs by. If None, lists all blobs.

    Returns:
        list[dict]: A list of dictionaries, each representing a blob with its name, size, and last modified date.
    """
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(container_name)

    blob_list = []
    for blob in container_client.list_blobs(name_starts_with=prefix):
        blob_list.append({
            "name": blob.name,
            "size": blob.size,
            "last_modified": blob.last_modified.isoformat() if blob.last_modified else None,
        })
    return blob_list
