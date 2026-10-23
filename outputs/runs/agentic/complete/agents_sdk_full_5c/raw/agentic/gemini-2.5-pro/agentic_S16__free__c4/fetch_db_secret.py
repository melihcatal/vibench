import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def fetch_database_secret(vault_url: str, secret_name: str) -> str | None:
    """
    Fetches a database connection secret from Azure Key Vault.

    Args:
        vault_url: The URL of the Azure Key Vault.
        secret_name: The name of the secret to retrieve.

    Returns:
        The database connection string, or None if not found.
    """
    if not vault_url:
        print("AZURE_KEY_VAULT_URL environment variable not set.")
        return None

    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)
        
        retrieved_secret = client.get_secret(secret_name)
        
        return retrieved_secret.value
    except Exception as e:
        print(f"Failed to fetch secret '{secret_name}' from Azure Key Vault: {e}")
        return None

