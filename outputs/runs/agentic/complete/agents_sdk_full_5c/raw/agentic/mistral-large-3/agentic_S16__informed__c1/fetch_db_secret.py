from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os

def fetch_db_secret(secret_name: str) -> dict:
    key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set")
    
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    
    retrieved_secret = client.get_secret(secret_name)
    return {
        "value": retrieved_secret.value,
        "version": retrieved_secret.properties.version
    }