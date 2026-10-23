from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os


def fetch_db_secret(secret_name: str, vault_url: str = None) -> str:
    """
    Fetch a database connection secret from Azure Key Vault.
    
    Args:
        secret_name: Name of the secret to fetch.
        vault_url: Azure Key Vault URL. Defaults to AZURE_KEY_VAULT_URL env var.
    
    Returns:
        The secret value as a string.
    """
    if vault_url is None:
        vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return secret.value