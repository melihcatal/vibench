import os
from typing import Any, Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_vault_url() -> str:
    url = os.getenv("AZURE_KEY_VAULT_URL")
    if not url:
        raise ValueError("AZURE_KEY_VAULT_URL is required")
    return url


def get_secret_client(vault_url: Optional[str] = None) -> SecretClient:
    return SecretClient(vault_url=vault_url or get_vault_url(), credential=DefaultAzureCredential())


def fetch_secret_value(name: str, version: Optional[str] = None, stage: Optional[str] = None) -> Any:
    client = get_secret_client()
    if stage:
        secret = client.get_secret(name, version=version) if version else client.get_secret(name)
    else:
        secret = client.get_secret(name, version=version)
    return secret.value
