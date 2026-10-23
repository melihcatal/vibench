from storage_client import StorageClient

def object_metadata(container_name: str, blob_name: str):
    client = StorageClient()
    blob_client = client.get_blob_client(container_name, blob_name)
    return blob_client.get_blob_properties()