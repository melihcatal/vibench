import os
from typing import Any, Dict, Optional

from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential


def get_key_vault_url() -> str:
    url = os.environ.get("AZURE_KEY_VAULT_URL")
    if not url:
        raise ValueError("AZURE_KEY_VAULT_URL is required")
    return url


def get_client() -> KeyClient:
    return KeyClient(vault_url=get_key_vault_url(), credential=DefaultAzureCredential())


def get_managed_key(key_name: str):
    return get_client().get_key(key_name)


def key_identifier(key_name: str, version: Optional[str] = None) -> str:
    base = get_key_vault_url().rstrip("/") + "/keys/" + key_name
    return f"{base}/{version}" if version else base


def build_aad(context: Optional[Dict[str, Any]] = None) -> bytes:
    if not context:
        return b""
    items = [f"{k}={v}" for k, v in sorted(context.items())]
    return "|".join(items).encode("utf-8")
