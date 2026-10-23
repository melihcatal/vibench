from storage_client import StorageClient

def object_metadata(connection_string: str, container_name: str, blob_name: str):
    client = StorageClient(connection_string)
    blob_client = client.get_blob_client(container_name, blob_name)
    return blob_client.get_blob_properties()