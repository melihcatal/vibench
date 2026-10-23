import os
from dataclasses import dataclass
from typing import Optional

from azure.core.credentials import AzureSasCredential
from azure.storage.blob import BlobServiceClient


@dataclass
class StorageConfig:
    account_url: str
    container: str
    credential: Optional[str] = None


def load_config(container: Optional[str] = None) -> StorageConfig:
    account_url = os.environ.get("AZURE_STORAGE_ACCOUNT_URL", "")
    resolved_container = container or os.environ.get("AZURE_STORAGE_CONTAINER", "")
    credential = os.environ.get("AZURE_STORAGE_SAS_TOKEN") or os.environ.get("AZURE_STORAGE_KEY")
    if not account_url or not resolved_container:
        raise ValueError("AZURE_STORAGE_ACCOUNT_URL and AZURE_STORAGE_CONTAINER are required")
    return StorageConfig(account_url=account_url, container=resolved_container, credential=credential)


def get_blob_service_client(config: Optional[StorageConfig] = None) -> BlobServiceClient:
    cfg = config or load_config()
    if cfg.credential:
        if cfg.credential.startswith("?") or "=" in cfg.credential:
            return BlobServiceClient(account_url=cfg.account_url, credential=AzureSasCredential(cfg.credential.lstrip("?")))
        return BlobServiceClient(account_url=cfg.account_url, credential=cfg.credential)
    return BlobServiceClient(account_url=cfg.account_url)


def normalize_blob_name(name: str) -> str:
    return name.lstrip("/")
