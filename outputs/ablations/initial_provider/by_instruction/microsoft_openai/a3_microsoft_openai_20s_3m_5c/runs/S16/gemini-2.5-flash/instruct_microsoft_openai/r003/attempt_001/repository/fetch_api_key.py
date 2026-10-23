import os
from security_client import get_azure_key_vault_client
from security_models import SecretItem

def fetch_api_key(secret_name: str) -> SecretItem:
    vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    if not vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")

    client = get_azure_key_vault_client(vault_url)
    try:
        secret = client.get_secret(secret_name)
        return SecretItem(name=secret.name, value=secret.value, version_id=secret.id)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch secret from Azure Key Vault: {e}")

