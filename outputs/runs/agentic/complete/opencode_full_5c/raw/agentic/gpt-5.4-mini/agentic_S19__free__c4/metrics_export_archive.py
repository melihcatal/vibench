from azure.storage.blob import BlobServiceClient

from observability_client import load_config


def metrics_export_archive(container_name, blob_name, payload):
    cfg = load_config()
    if cfg.azure_storage_connection_string:
        client = BlobServiceClient.from_connection_string(
            cfg.azure_storage_connection_string
        )
    else:
        client = BlobServiceClient(account_url=cfg.azure_storage_account_url)
    blob = client.get_blob_client(container=container_name, blob=blob_name)
    blob.upload_blob(payload, overwrite=True)
    return {
        "container": container_name,
        "blob": blob_name,
        "provider": "azure_blob_storage",
    }
