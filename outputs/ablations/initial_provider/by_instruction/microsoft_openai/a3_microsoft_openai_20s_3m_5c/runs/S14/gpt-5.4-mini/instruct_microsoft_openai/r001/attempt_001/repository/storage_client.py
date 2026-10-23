import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import AzureOpenAI


@dataclass
class StorageConfig:
    account_url: str
    container_name: str
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_api_version: str
    azure_openai_deployment: str


def load_storage_config() -> StorageConfig:
    return StorageConfig(
        account_url=os.environ["AZURE_STORAGE_ACCOUNT_URL"],
        container_name=os.environ["AZURE_STORAGE_CONTAINER"],
        azure_openai_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_openai_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    )


def get_azure_openai_client(config: Optional[StorageConfig] = None) -> AzureOpenAI:
    cfg = config or load_storage_config()
    return AzureOpenAI(
        azure_endpoint=cfg.azure_openai_endpoint,
        api_key=cfg.azure_openai_api_key,
        api_version=cfg.azure_openai_api_version,
    )


def resolve_container_path(blob_name: str, config: Optional[StorageConfig] = None) -> str:
    cfg = config or load_storage_config()
    return f"{cfg.account_url.rstrip('/')}/{cfg.container_name}/{blob_name.lstrip('/')}"


def coerce_bytes(data: Any) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if hasattr(data, "read"):
        value = data.read()
        return value if isinstance(value, bytes) else str(value).encode("utf-8")
    return str(data).encode("utf-8")
