import os
import json

# Azure Key Vault Secrets integration
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Configuration (normally loaded from env or config file)
AZURE_KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL")
API_KEY_SECRET_NAME = "my-api-key"


def fetch_api_key() -> str:
    """Fetches an API key stored as a secret in Azure Key Vault.
    Returns:
        The raw API key string.
    Raises:
        RuntimeError: If the secret cannot be retrieved.
    """
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=AZURE_KEY_VAULT_URL, credential=credential)
    retrieved = client.get_secret(API_KEY_SECRET_NAME)
    return retrieved.value
