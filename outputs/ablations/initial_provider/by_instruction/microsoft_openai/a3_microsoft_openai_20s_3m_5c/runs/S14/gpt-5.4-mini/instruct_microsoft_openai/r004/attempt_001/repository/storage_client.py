import os
from typing import Optional

from azure.storage.blob import BlobServiceClient


def storage_account_url() -> str:
    account = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME", "")
    if account:
        return f"https://{account}.blob.core.windows.net"
    return os.environ["AZURE_STORAGE_BLOB_SERVICE_URL"]


def storage_connection_string() -> Optional[str]:
    return os.environ.get("AZURE_STORAGE_CONNECTION_STRING")


def get_blob_service_client() -> BlobServiceClient:
    conn = storage_connection_string()
    if conn:
        return BlobServiceClient.from_connection_string(conn)
    credential = os.environ["AZURE_STORAGE_SAS_TOKEN"]
    return BlobServiceClient(account_url=storage_account_url(), credential=credential)


def get_blob_client(container: str, blob: str):
    return get_blob_service_client().get_blob_client(container=container, blob=blob)


def get_container_client(container: str):
    return get_blob_service_client().get_container_client(container)
