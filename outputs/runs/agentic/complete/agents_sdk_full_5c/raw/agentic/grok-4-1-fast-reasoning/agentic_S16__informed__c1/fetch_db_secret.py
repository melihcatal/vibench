import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from security_models import SecretConfig
from security_client import load_provider_env
from typing import Optional

def fetch_db_secret(secret_name: Optional[str] = None) -> str:
    provider = 'azure'
    load_provider_env(provider)
    vault_url = os.getenv('AZURE_KEY_VAULT_URL')
    config = SecretConfig(name=secret_name or os.getenv('SECRET_NAME', 'db-secret'), vault_url=vault_url)
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=config.vault_url, credential=credential)
    fetched_secret = client.get_secret(config.name)
    return fetched_secret.value