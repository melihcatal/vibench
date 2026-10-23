import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def get_secret_client() -> SecretClient:
    key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    return client
