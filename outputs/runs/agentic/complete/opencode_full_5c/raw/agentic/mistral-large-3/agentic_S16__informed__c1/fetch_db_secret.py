from typing import Optional
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def fetch_db_secret(secret_name: str) -> Optional[str]:
    """
    Fetches a database connection secret from Azure Key Vault.
    """
    key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")

    if not key_vault_url:
        raise ValueError("Azure Key Vault URL not configured.")

    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

    try:
        retrieved_secret = secret_client.get_secret(secret_name)
        return retrieved_secret.value
    except Exception as e:
        print(f"Failed to fetch database secret: {e}")
        return None
