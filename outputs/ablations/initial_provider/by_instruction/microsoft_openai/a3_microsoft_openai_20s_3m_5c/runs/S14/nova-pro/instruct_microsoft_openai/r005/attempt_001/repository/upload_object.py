from storage_client import StorageClient

def upload_object(connection_string: str, container_name: str, blob_name: str, data: bytes):
    client = StorageClient(connection_string)
    blob_client = client.get_blob_client(container_name, blob_name)
    blob_client.upload_blob(data, overwrite=True)