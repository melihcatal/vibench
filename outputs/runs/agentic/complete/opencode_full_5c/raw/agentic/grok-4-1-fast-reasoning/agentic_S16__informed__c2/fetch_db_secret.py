from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from security_client import get_azure_vault_url
from security_models import parse_db_secret
from typing import Dict, Any


def fetch_db_secret(secret_name: str) -> Dict[str, Any]:
    vault_url = get_azure_vault_url()
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    kv_secret = client.get_secret(secret_name)
    return parse_db_secret(kv_secret.value)
