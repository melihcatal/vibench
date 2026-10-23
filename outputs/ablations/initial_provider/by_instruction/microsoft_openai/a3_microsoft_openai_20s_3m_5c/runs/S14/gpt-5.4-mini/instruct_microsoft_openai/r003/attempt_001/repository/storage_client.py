import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

from azure.storage.blob import BlobServiceClient


@dataclass
class StorageConfig:
    account_url: str
    credential: Optional[str] = None
    container_name: Optional[str] = None


def load_storage_config() -> StorageConfig:
    return StorageConfig(
        account_url=os.environ["AZURE_STORAGE_ACCOUNT_URL"],
        credential=os.getenv("AZURE_STORAGE_CONNECTION_STRING") or os.getenv("AZURE_STORAGE_SAS_TOKEN") or os.getenv("AZURE_STORAGE_ACCOUNT_KEY"),
        container_name=os.getenv("AZURE_STORAGE_CONTAINER_NAME"),
    )


def get_blob_service_client() -> BlobServiceClient:
    cfg = load_storage_config()
    if cfg.credential:
        return BlobServiceClient(account_url=cfg.account_url, credential=cfg.credential)
    return BlobServiceClient(account_url=cfg.account_url)


def get_container_name(container_name: Optional[str] = None) -> str:
    if container_name:
        return container_name
    cfg = load_storage_config()
    if not cfg.container_name:
        raise ValueError("AZURE_STORAGE_CONTAINER_NAME is required")
    return cfg.container_name


def normalize_bytes(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, str):
        return data.encode("utf-8")
    if hasattr(data, "read"):
        return data.read()
    raise TypeError("Unsupported upload payload")


def to_dict(metadata: Any) -> Dict[str, Any]:
    if metadata is None:
        return {}
    if isinstance(metadata, dict):
        return metadata
    if hasattr(metadata, "items"):
        return dict(metadata.items())
    return {k: getattr(metadata, k) for k in dir(metadata) if not k.startswith("_")}
