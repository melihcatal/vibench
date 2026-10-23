import os
from dataclasses import dataclass
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


@dataclass(frozen=True)
class SecretManagerConfig:
    key_vault_url: str
    credential: DefaultAzureCredential


def load_secret_manager_config() -> SecretManagerConfig:
    key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL is required")
    return SecretManagerConfig(key_vault_url=key_vault_url, credential=DefaultAzureCredential())


def create_secret_client(config: Optional[SecretManagerConfig] = None) -> SecretClient:
    if config is None:
        config = load_secret_manager_config()
    return SecretClient(vault_url=config.key_vault_url, credential=config.credential)


def get_secret_value(secret_name: str, version: Optional[str] = None) -> str:
    client = create_secret_client()
    secret = client.get_secret(secret_name, version=version)
    return secret.value


def set_secret_value(secret_name: str, secret_value: str) -> str:
    client = create_secret_client()
    secret = client.set_secret(secret_name, secret_value)
    return secret.id
