from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os

from security_client import get_vault_url
from security_models import SecretResponse

def fetch_api_key(secret_name: str) -> SecretResponse:
    vault_url = get_vault_url()
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    retrieved_secret = client.get_secret(secret_name)
    return SecretResponse(
        name=retrieved_secret.name,
        value=retrieved_secret.value,
        version=retrieved_secret.properties.version,
        enabled=retrieved_secret.properties.enabled
    )