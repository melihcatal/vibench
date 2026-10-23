import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def fetch_db_secret(secret_name: str) -> str:
    key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)

    try:
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        raise RuntimeError(f"Error fetching DB secret '{secret_name}' from Azure Key Vault: {e}")
