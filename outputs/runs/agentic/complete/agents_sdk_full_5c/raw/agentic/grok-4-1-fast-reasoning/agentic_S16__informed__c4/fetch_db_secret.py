from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os
from security_client import get_azure_vault_url
from security_models import DBSecret, parse_db_secret

def fetch_db_secret(secret_name: str) -> DBSecret:
    vault_url = get_azure_vault_url()
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret_bundle = client.get_secret(secret_name)
    return parse_db_secret(secret_bundle.value)
