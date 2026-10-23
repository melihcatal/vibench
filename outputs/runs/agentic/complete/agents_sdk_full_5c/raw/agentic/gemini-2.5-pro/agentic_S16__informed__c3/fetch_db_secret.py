import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from security_client import get_azure_credential

def get_secret_client(vault_url):
    credential = get_azure_credential()
    if not credential:
        # Fallback for local dev if environment not fully set up
        credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client

def fetch_database_secret(secret_name: str) -> str | None:
    """
    Fetches a database connection string from Azure Key Vault.

    Args:
        secret_name: The name of the secret to retrieve.

    Returns:
        The secret value, or None if not found.
    """
    vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    if not vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")

    try:
        client = get_secret_client(vault_url)
        retrieved_secret = client.get_secret(secret_name)
        return retrieved_secret.value
    except Exception as e:
        print(f"Failed to fetch secret '{secret_name}' from Azure Key Vault: {e}")
        return None
