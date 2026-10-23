from storage_client import StorageClient

def presigned_download(connection_string: str, container_name: str, blob_name: str, expiry: int = 3600):
    client = StorageClient(connection_string)
    blob_client = client.get_blob_client(container_name, blob_name)
    sas_token = blob_client.generate_blob_sas(permission='r', expiry=expiry)
    return blob_client.url + '?' + sas_token