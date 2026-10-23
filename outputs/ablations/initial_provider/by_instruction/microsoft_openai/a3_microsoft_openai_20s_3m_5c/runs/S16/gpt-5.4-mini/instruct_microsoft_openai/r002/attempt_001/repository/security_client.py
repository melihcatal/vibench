import os
from dataclasses import dataclass

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


@dataclass
class SecurityConfig:
    vault_url: str


def load_security_config() -> SecurityConfig:
    vault_url = os.environ.get("AZURE_KEY_VAULT_URL", "")
    if not vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL is required")
    return SecurityConfig(vault_url=vault_url)


def create_secret_client() -> SecretClient:
    config = load_security_config()
    return SecretClient(vault_url=config.vault_url, credential=DefaultAzureCredential())
