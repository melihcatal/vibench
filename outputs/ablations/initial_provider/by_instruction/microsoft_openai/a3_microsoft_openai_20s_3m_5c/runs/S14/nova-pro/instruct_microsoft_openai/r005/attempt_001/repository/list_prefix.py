from storage_client import StorageClient

def list_prefix(connection_string: str, container_name: str, prefix: str):
    client = StorageClient(connection_string)
    container_client = client.get_container_client(container_name)
    blob_list = container_client.list_blobs(name_starts_with=prefix)
    return [blob.name for blob in blob_list]