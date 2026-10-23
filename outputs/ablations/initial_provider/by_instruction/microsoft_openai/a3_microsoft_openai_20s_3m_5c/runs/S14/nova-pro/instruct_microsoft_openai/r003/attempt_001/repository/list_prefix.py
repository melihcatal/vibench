from storage_client import StorageClient

def list_prefix(container_name: str, prefix: str):
    client = StorageClient()
    container_client = client.get_container_client(container_name)
    blob_list = container_client.list_blobs(name_starts_with=prefix)
    return [blob.name for blob in blob_list]