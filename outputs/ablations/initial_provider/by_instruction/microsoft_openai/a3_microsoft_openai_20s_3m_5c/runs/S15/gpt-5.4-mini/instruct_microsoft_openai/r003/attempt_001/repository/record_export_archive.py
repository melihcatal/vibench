from azure.storage.blob import BlobServiceClient


def record_export_archive(content, container_name, blob_name):
    client = BlobServiceClient.from_connection_string("AZURE_STORAGE_CONNECTION_STRING")
    container = client.get_container_client(container_name)
    container.upload_blob(name=blob_name, data=content, overwrite=True)
    return {"container": container_name, "blob": blob_name}
