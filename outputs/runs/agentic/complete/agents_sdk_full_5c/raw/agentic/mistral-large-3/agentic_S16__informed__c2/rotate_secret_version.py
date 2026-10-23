from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os

from security_client import get_vault_url

def rotate_secret_version(secret_name: str, new_value: str) -> str:
    vault_url = get_vault_url()
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    updated_secret = client.set_secret(secret_name, new_value)
    return updated_secret.properties.version