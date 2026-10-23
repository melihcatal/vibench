import os
from dataclasses import dataclass
from typing import Optional

from azure.core.credentials import AzureNamedKeyCredential, AzureSasCredential
from azure.storage.blob import BlobServiceClient


@dataclass
class StorageConfig:
    account_url: str
    container_name: Optional[str] = None
    account_name: Optional[str] = None
    account_key: Optional[str] = None
    sas_token: Optional[str] = None
    connection_string: Optional[str] = None


def load_storage_config() -> StorageConfig:
    return StorageConfig(
        account_url=os.environ.get("AZURE_STORAGE_ACCOUNT_URL", ""),
        container_name=os.environ.get("AZURE_STORAGE_CONTAINER_NAME"),
        account_name=os.environ.get("AZURE_STORAGE_ACCOUNT_NAME"),
        account_key=os.environ.get("AZURE_STORAGE_ACCOUNT_KEY"),
        sas_token=os.environ.get("AZURE_STORAGE_SAS_TOKEN"),
        connection_string=os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
    )


def build_blob_service_client(config: Optional[StorageConfig] = None) -> BlobServiceClient:
    config = config or load_storage_config()
    if config.connection_string:
        return BlobServiceClient.from_connection_string(config.connection_string)
    if config.sas_token:
        return BlobServiceClient(account_url=config.account_url, credential=AzureSasCredential(config.sas_token))
    if config.account_name and config.account_key:
        return BlobServiceClient(account_url=config.account_url, credential=AzureNamedKeyCredential(config.account_name, config.account_key))
    return BlobServiceClient(account_url=config.account_url)


def normalize_container_name(container_name: Optional[str], config: Optional[StorageConfig] = None) -> str:
    if container_name:
        return container_name
    config = config or load_storage_config()
    if not config.container_name:
        raise ValueError("AZURE_STORAGE_CONTAINER_NAME is required")
    return config.container_name
