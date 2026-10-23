import os
from security_client import get_azure_key_vault_secret_client
from security_models import Secret

def fetch_api_key(secret_name: str) -> Secret:
    vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    if not vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")
    
    client = get_azure_key_vault_secret_client(vault_url)
    azure_secret = client.get_secret(secret_name)
    return Secret(name=azure_secret.name, value=azure_secret.value)

