from storage_client import StorageClient

def presigned_download(container_name: str, blob_name: str, expiration: int):
    client = StorageClient()
    blob_client = client.get_blob_client(container_name, blob_name)
    sas_token = blob_client.get_blob_client().get_blob_client().generate_blob_sas(permission='r', expiry=expiration)
    return blob_client.url + '?' + sas_token